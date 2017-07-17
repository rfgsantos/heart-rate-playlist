package com.tomazinhal.broadcastreceiver;

import android.content.Context;
import android.content.Intent;
import android.util.Log;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

/**
 * Created by Tomazinhal on 27/05/2017.
 */

public class Reaction{
    private static Reaction rInstance = null;
    private Context mContext = null;

    private String TAG = "REACTION Class";

    private SimpleDateFormat dateFormat;

    private String userId = "11122241033";
    private String trackId = null;
    private String location = "here";
    private List<Float> heartRate = null;

    public boolean playback = false;

    private Reaction(){}

    public void init(Context context){
        mContext = context;
        this.userId = "11122241033";
        this.trackId = null;
        this.dateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault());
        this.location = "here";
        this.heartRate = new ArrayList<Float>();
    }

    public static Reaction getInstance(){
        if(rInstance == null){
            rInstance = new Reaction();
        }
        return rInstance;
    }

    public String getUserId() {
        return userId;
    }

    public String getTrackId() {
        return trackId;
    }

    public List<Float> getHeartRate() {
        return heartRate;
    }

    public String getDatetime() {
        return dateFormat.getDateTimeInstance().format(new Date());
    }

    public String getLocation() {
        return location;
    }

    public boolean addHeartRate(List<Float> heartRate){
        boolean success = false;
        if(playback){
            success = true;
            //heart rate corresponds to playing track
            for(Float rate : heartRate){
                success = success & this.addHeartRate(rate);
            }
        }else{
            success = false;
        }
        return success;
    }

    public boolean addHeartRate(Float heartRate){
        boolean success = this.heartRate.add(heartRate);
        return success;
    }

    public void setTrackId(String trackId){
        if (!trackId.equals(this.trackId)){
            if(this.trackId != null){
                Log.i(TAG, "Sending previous reaction to handle new one.");
                send();
                reset();
            }
            this.trackId = trackId;
        } else { //It's the same track, somehow
            return;
        }
    }

    public void send(){
        Intent intent = new Intent();
        intent.setAction("com.tomazinhal.broadcastreceiver.Reaction");
        intent.putExtra("userId", userId);
        intent.putExtra("trackId", trackId);
        intent.putExtra("location", location);
        intent.putExtra("dateTime", getDatetime());
        intent.putExtra("heartRate", listToArray(this.heartRate));
        mContext.sendBroadcast(intent);
    }

    private float[] listToArray(List<Float> list){
        float[] array = new float[list.size()];
        int i = 0;
        for (Float f : list) {
            array[i++] = (f != null ? f : Float.NaN);
        }
        return array;
    }

    public void setPlayback(boolean playback){
        if(playback == this.playback){
            Log.i(TAG, "Already playing - " + this.trackId);
            return;
        }
        this.playback = playback;

    }

    public void reset(){
        userId = "11122241033";
        trackId = null;
        location = "here";
        heartRate = new ArrayList<Float>();
    }
}