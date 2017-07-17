package com.tomazinhal.broadcastreceiver;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;
import android.widget.Toast;

import com.tomazinhal.broadcastreceiver.MainActivity;
import com.tomazinhal.broadcastreceiver.Reaction;
import com.tomazinhal.broadcastreceiver.webservice.ReactionAPI;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

/**
 * Created by Tomazinhal on 12/06/2017.
 */

public class ReactionReceiver extends BroadcastReceiver {
    private String TAG = "REACTION Receiver";
    static final String REACTION = "com.tomazinhal.broadcastreceiver.Reaction";

    public String port = "5000";
    public String host = "192.168.1.9";

    final String serverURL = "http://" + host + ":" + port + "/";
    private Retrofit.Builder builder = new Retrofit.Builder()
            .baseUrl(this.serverURL)
            .addConverterFactory(GsonConverterFactory.create());
    public Retrofit retrofit = builder.build();

    @Override
    public void onReceive(Context context, Intent intent) {
        Log.i(TAG, "Action: " + intent.getAction());
        String rUserId = (String) intent.getExtras().get("userId");
        Log.i(TAG, "User ID: " + rUserId);
        String rTrackId = (String) intent.getExtras().get("trackId");
        Log.i(TAG, "Track ID: " + rTrackId);
        String rLocation = (String) intent.getExtras().get("location");
        Log.i(TAG, "Location: " + rLocation);
        String rDatetime = (String) intent.getExtras().get("dateTime");
        Log.i(TAG, "Date: " + rDatetime);
        float[] array;
        if (intent.getExtras().getFloatArray("heartRate") != null){
            array = intent.getExtras().getFloatArray("heartRate");
        }else{
            array = new float[]{};
        }
        List<Float> rHeartRate = arrayToList(array);

        ReactionAPI reactionAPI = retrofit.create(ReactionAPI.class);
        Call<ResponseBody> call = reactionAPI.sendNewReaction(
                rUserId,
                rTrackId,
                rDatetime,
                rLocation,
                rHeartRate
        );

        call.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
                Log.i(TAG, "SUCCESS! Reaction sent.");
            }
            @Override
            public void onFailure(Call<ResponseBody> call, Throwable t) {
                Log.i(TAG, "FAIL! Reaction not sent.");
            }
        });
    }

    private List<Float> arrayToList(float[] array){
        List<Float> list = new ArrayList<Float>(array.length);
        for(float f : array){
            list.add(f);
        }
        return list;
    }

    private String listToString(List<Float> list){
        final StringBuilder builder = new StringBuilder();
        for (final Float interval : list)
            builder.append(String.format("%.02f ms, ", interval));
        builder.setLength(builder.length() - 2); // remove the ", " at the end
        return builder.toString();
    }

}
