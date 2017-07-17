/*
 * Copyright (c) 2015, Nordic Semiconductor
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this
 * software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

package com.tomazinhal.broadcastreceiver;
import com.tomazinhal.broadcastreceiver.webservice.ReactionAPI;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattDescriptor;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothProfile;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class MainActivity extends AppCompatActivity implements BluetoothAdapter.LeScanCallback{

    private Button dataBtn;
    private EditText URLTxt;

    //BLUETOOTH VARIABLES
    private Handler mHandler;
    private static int REQUEST_ENABLE_BT = 1;
    private static int SCAN_PERIOD = 5000;
    private static final String TAG = "GATT Activity";
    private static final String DEVICE_NAME = "CardioWheel";//"Nordic_HRM";
    //Heart Rate Service
    private static final UUID HEART_RATE_SERVICE        = UUID.fromString("0000180d-0000-1000-8000-00805f9b34fb");
    private static final UUID HEART_RATE_CHARACTERISTIC = UUID.fromString("00002a37-0000-1000-8000-00805f9b34fb");
    private static final UUID CONFIG_DESCRIPTOR         = UUID.fromString("00002902-0000-1000-8000-00805f9b34fb");

    private BluetoothAdapter mBluetoothAdapter;
    private BluetoothDevice nordicBLE;
    private BluetoothGatt mConnectedGatt;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Reaction.getInstance().init(this);

        URLTxt = (EditText) findViewById(R.id.editURL);
        /*
        dataBtn = (Button) findViewById(R.id.btnData);
        dataBtn.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v){
                sendReaction(Reaction.getInstance());
            }
        });
        */

        mHandler = new Handler();
        startBluetooth();
    }

    @Override
    protected void onResume() {
        super.onResume();
        startBluetooth();
        startScan();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Reaction reaction = Reaction.getInstance();
        reaction.reset();
    }

    @Override
    protected void onPause() {
        super.onPause();
        stopScan();
        mHandler.removeCallbacks(mStartScan);
        mHandler.removeCallbacks(mStopScan);
        mBluetoothAdapter.stopLeScan(this);
    }

    public void startBluetooth(){
        if (!getPackageManager().hasSystemFeature(PackageManager.FEATURE_BLUETOOTH_LE)) {
            Toast.makeText(this, "BLE Not Supported",
                    Toast.LENGTH_SHORT).show();
            finish();
        }
        BluetoothManager manager = (BluetoothManager) getSystemService(BLUETOOTH_SERVICE);
        mBluetoothAdapter = manager.getAdapter();

        if (mBluetoothAdapter == null || !mBluetoothAdapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
        }
    }

    public void enableHeartRateSensor(BluetoothGatt gatt){
        BluetoothGattCharacteristic characteristic = gatt.getService(HEART_RATE_SERVICE)
                .getCharacteristic(HEART_RATE_CHARACTERISTIC);
        if(characteristic != null) {
            //Set Heart Rate Measurement characteristic according to https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.characteristic.heart_rate_measurement.xml
            characteristic.setValue(new byte[] {0x11}); //RR Interval UINT16 - 17 | 0001 0001 | 0x11
            gatt.writeCharacteristic(characteristic);
            Log.i(TAG, "Enabling heart rate sensor.");
        }else{
            Log.i(TAG, "Couldn't enable sensor.");
        }
    }

    //Never runs because onCharacteristicWrite is never triggered.
    public void readHeartRateSensor(BluetoothGatt gatt){
        Log.i(TAG, "Reading first characteristic.");
        BluetoothGattCharacteristic characteristic = gatt.getService(HEART_RATE_SERVICE)
                .getCharacteristic(HEART_RATE_CHARACTERISTIC);
        gatt.readCharacteristic(characteristic);
    }

    public void setHeartRateNotification(BluetoothGatt gatt){
        Log.i(TAG, "Setting up notifications for heart rate sensor.");
        BluetoothGattCharacteristic characteristic;
        characteristic = gatt.getService(HEART_RATE_SERVICE)
                .getCharacteristic(HEART_RATE_CHARACTERISTIC);
        //Enable local notifications
        gatt.setCharacteristicNotification(characteristic, true);
        //Enable remote notifications
        BluetoothGattDescriptor desc = characteristic.getDescriptor(CONFIG_DESCRIPTOR);
        desc.setValue(BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE);
        gatt.writeDescriptor(desc);
    }

    public void parseHeartRate(BluetoothGattCharacteristic characteristic){
        //Most of this code from Nordic Semiconductor, therefore the above copyright notice.
        byte HEART_RATE_VALUE_FORMAT = 0x01; // 1 bit
        byte RR_INTERVAL = 0x10; // 1 bit

        int offset = 0;

        int flags = characteristic.getIntValue(BluetoothGattCharacteristic.FORMAT_UINT8, offset++);

        boolean value16bit = (flags & HEART_RATE_VALUE_FORMAT) > 0;
        boolean rrIntervalStatus = (flags & RR_INTERVAL) > 0;

        int heartRateValue = characteristic.getIntValue(value16bit ? BluetoothGattCharacteristic.FORMAT_UINT16 : BluetoothGattCharacteristic.FORMAT_UINT8, offset++);
        if (value16bit) {
            //Log.i(TAG, "Heart rate format UINT16.");
            offset++;
        }

        final List<Float> rrIntervals = new ArrayList<>();
        if (rrIntervalStatus) {
            //Log.i(TAG, "RR-Intervals available.");
            int units = characteristic.getIntValue(BluetoothGattCharacteristic.FORMAT_UINT16, offset);
            rrIntervals.add(units * 1000.0f / 1024.0f);
            Log.i(TAG, "RR-Interval: " + units);
            /*);
            for (int o = offset; o < characteristic.getValue().length; o += 2) {
                final int units = characteristic.getIntValue(BluetoothGattCharacteristic.FORMAT_UINT16, o);
                rrIntervals.add(units * 1000.0f / 1024.0f); // RR interval is in [1/1024s]
            }*/
        }

        final StringBuilder builder = new StringBuilder();
        builder.append("Heart Rate Measurement: ").append(heartRateValue).append(" bpm");
        if (rrIntervalStatus) {
            builder.append(",\nRR Interval: ");
            for (final Float interval : rrIntervals)
                builder.append(String.format("%.02f ms, ", interval));
            builder.setLength(builder.length() - 2); // remove the ", " at the end
        }
        Log.i(TAG, builder.toString());


        Reaction reaction = Reaction.getInstance();
        reaction.addHeartRate(rrIntervals);
    }

    @Override
    public void onLeScan(BluetoothDevice device, int rssi, byte[] scanRecord) {
        Log.i(TAG, "New device: " + device.getName() + " @ " + rssi);
        if (DEVICE_NAME.equals(device.getName())/* || device.getName().equals("Nordic_HRM")*/){
            Log.i(TAG, "Found Nordic_HRM - Heart Rate Monitor.");
            nordicBLE = device;
            mConnectedGatt = device.connectGatt(this, false, mGattCallback);
        }
    }

    private Runnable mStartScan = new Runnable(){
        @Override
        public void run(){
            startScan();
            mHandler.postDelayed(mStopScan, SCAN_PERIOD);
        }
    };
    private Runnable mStopScan = new Runnable(){
        @Override
        public void run(){
            stopScan();
        }
    };

    private void startScan(){
        UUID[] uuids = new UUID[]{HEART_RATE_SERVICE};
        mBluetoothAdapter.startLeScan(uuids, this);
    }

    private void stopScan(){
        mBluetoothAdapter.stopLeScan(this);
    }

    private BluetoothGattCallback mGattCallback = new BluetoothGattCallback() {

        @Override
        public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState) {
            if(status == BluetoothGatt.GATT_SUCCESS && newState == BluetoothProfile.STATE_CONNECTED) {
                //Successfully connected. Now I have to discover all services before
                //I can read and write characteristics.
                Log.i(TAG, "Successfully connected to " + DEVICE_NAME + ".");
                stopScan();
                gatt.discoverServices();
                Log.i(TAG, "Discovering services.");
            } else if (status == BluetoothGatt.GATT_SUCCESS && newState == BluetoothGatt.STATE_DISCONNECTED){
                //For some reason the device is disconnected.
                Log.i(TAG, "Disconnecting...");
            } else if (status != BluetoothGatt.GATT_SUCCESS){
                //If something fails then disconnect.
                gatt.disconnect();
            }
        }

        @Override
        public void onServicesDiscovered(BluetoothGatt gatt, int status) {
            if (status == gatt.GATT_SUCCESS){
                Log.i(TAG, "Discovered services!");
                enableHeartRateSensor(gatt);
                setHeartRateNotification(gatt);
            }
        }

        @Override //This doesn't trigger because ...TODO
        public void onCharacteristicWrite(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic, int status) {
            Log.i(TAG, "Attempting to write characteristic.");
            if(status == gatt.GATT_SUCCESS){
                Log.i(TAG, "Wrote characteristic.");
                readHeartRateSensor(gatt);
            }else{
                Log.i(TAG, "Characteristic: " + characteristic.getUuid().toString());
                Log.i(TAG, "Couldn't write characteristic.");
            }
        }

        @Override
        public void onCharacteristicRead(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic, int status) {
            if(status == gatt.GATT_SUCCESS) {
                if (HEART_RATE_CHARACTERISTIC.equals(characteristic.getUuid())) {
                    Log.i(TAG, "Read heart rate from heart rate characteristic.");
                    parseHeartRate(characteristic);
                } else {
                    Log.i(TAG, "Read another characteristic");
                }
                setHeartRateNotification(gatt);
            }
        }

        @Override
        public void onCharacteristicChanged(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic) {
            if(HEART_RATE_CHARACTERISTIC.equals(characteristic.getUuid())){
                // Log.i(TAG, "Read heart rate from a device after enabling notifications.");
                parseHeartRate(characteristic);
            }
        }
    };

    /*
    void sendReaction(Reaction reaction) {
        String userId = reaction.getUserId();
        String trackId = reaction.getTrackId();
        String rLocation = reaction.getLocation();
        String rDatetime = reaction.getDatetime();
        List<Float> rHeartRate = reaction.getHeartRate();

        ReactionAPI reactionAPI = retrofit.create(ReactionAPI.class);

        Call<ResponseBody> call = reactionAPI.sendNewReaction(
                userId,
                trackId,
                rDatetime,
                rLocation,
                rHeartRate
        );

        call.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
                Toast.makeText(MainActivity.this, "Success", Toast.LENGTH_SHORT).show();
            }
            @Override
            public void onFailure(Call<ResponseBody> call, Throwable t) {
                Toast.makeText(MainActivity.this, "Fail", Toast.LENGTH_SHORT).show();
            }
        });
    }
    */
}
