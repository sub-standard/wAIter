package com.substandard.waiter

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.uriio.beacons.Beacons

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.main_activity)
        Beacons.initialize(this);
    }
}
