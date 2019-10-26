package com.substandard.waiter

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.mongodb.stitch.android.core.Stitch
import com.mongodb.stitch.core.auth.providers.anonymous.AnonymousCredential
import com.uriio.beacons.Beacons

class MainActivity : AppCompatActivity() {
    val client = Stitch.getDefaultAppClient()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.main_activity)
        Beacons.initialize(this)
        client.auth.loginWithCredential(AnonymousCredential())
    }
}
