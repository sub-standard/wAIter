package com.substandard.waiter.ui.main

import androidx.lifecycle.ViewModel
import com.substandard.waiter.Drinks
import com.substandard.waiter.MongoClient
import com.uriio.beacons.model.iBeacon

class MainViewModel : ViewModel() {
    private val id = "abcdefghijklmnop"

    private var orderDrinks: Drinks? = null

    private val beacon =
        iBeacon(id.toByteArray(), 0, 0, "wAIter")

    private val mongo = MongoClient()

    fun startBeacon() = beacon.start()

    fun stopBeacon() = beacon.stop()

    fun setOrder(order: Drinks) {
        orderDrinks = order
    }

    fun getOrder(): Drinks? {
        return orderDrinks
    }
}
