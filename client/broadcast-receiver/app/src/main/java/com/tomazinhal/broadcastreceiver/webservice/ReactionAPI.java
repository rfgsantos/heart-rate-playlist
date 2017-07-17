package com.tomazinhal.broadcastreceiver.webservice;

import android.content.Intent;

import java.util.List;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Field;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.POST;

/**
 * Created by Tomazinhal on 27/05/2017.
 */

public interface ReactionAPI {

    @FormUrlEncoded
    @POST("new_reaction")
    Call<ResponseBody> sendNewReaction(@Field("user_id") String userID,
                                       @Field("track_id") String trackId,
                                       @Field("datetime") String datetime,
                                       @Field("location") String location,
                                       @Field("heart_rate") List<Float> heartRate);
}
