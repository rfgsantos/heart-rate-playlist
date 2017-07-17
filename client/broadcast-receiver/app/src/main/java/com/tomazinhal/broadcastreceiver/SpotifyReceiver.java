package com.tomazinhal.broadcastreceiver;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;
import android.widget.Toast;

/**
 * Created by Tomazinhal on 24/05/2017.
 */

public class SpotifyReceiver extends BroadcastReceiver {
    private static String TAG = "SPOTIFY Receiver";


    static final class BroadcastTypes {
        static final String SPOTIFY_PACKAGE = "com.spotify.music";
        static final String PLAYBACK_STATE_CHANGED = SPOTIFY_PACKAGE + ".playbackstatechanged";
        static final String METADATA_CHANGED = SPOTIFY_PACKAGE + ".metadatachanged";
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        Toast.makeText(context, "Intent Detected.", Toast.LENGTH_SHORT).show();

        Reaction reaction = Reaction.getInstance();

        String action = intent.getAction();
        if (action.equals(BroadcastTypes.METADATA_CHANGED)) {
            String trackId = intent.getStringExtra("id");
            Log.i(TAG, "Extras: " + intent.getExtras().toString());
            Log.i(TAG, "Spotify Broadcast: " + trackId);
            reaction.setTrackId(trackId);
            /*
            Intent intentService = new Intent(context, SpotifyReceiver.class);
            // add infos for the service which file to download and where to store
            intentService.putExtra("trackId", trackId);
            context.startService(intentService);
            */
        } else if (action.equals(BroadcastTypes.PLAYBACK_STATE_CHANGED)) {
            boolean playing = intent.getBooleanExtra("playing", false);
            Log.i(TAG, "Playing: " + playing);
            int positionInMs = intent.getIntExtra("playbackPosition", 0);
            reaction.setPlayback(playing);
        }
    }
}