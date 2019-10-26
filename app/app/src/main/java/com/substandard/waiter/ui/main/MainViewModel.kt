package com.substandard.waiter.ui.main

import androidx.lifecycle.ViewModel
import com.uriio.beacons.model.iBeacon


class MainViewModel : ViewModel() {
    private val id = "abcdefghijklmnop"

    private val beacon =
        iBeacon(id.toByteArray(), 0, 0, "wAIter")

    fun startBeacon() = beacon.start()

    fun stopBeacon() = beacon.stop()
}
