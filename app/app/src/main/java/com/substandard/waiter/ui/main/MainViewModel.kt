package com.substandard.waiter.ui.main

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.substandard.waiter.Drinks
import com.substandard.waiter.MongoClient
import com.uriio.beacons.model.iBeacon

class MainViewModel : ViewModel() {
    private val id = "abcdefghijklmnop"

    private var orderDrinks: Drinks? = null

    private var orderId: String? = null

    private val beacon =
        iBeacon(id.toByteArray(), 0, 0, "wAIter")

    private val mongo = MongoClient()

    private val _status = MutableLiveData("none")
    val status: LiveData<String> = _status

    fun startBeacon() = beacon.start()

    fun stopBeacon() = beacon.stop()

    fun setOrder(order: Drinks) {
        orderDrinks = order
    }

    fun getOrder(): Drinks? {
        return orderDrinks
    }

    fun orderDelivered() {
        stopBeacon()

        mongo.client.callFunction("set_delivered", listOf(orderId)).addOnCompleteListener {
            _status.postValue("delivered")
        }
    }
}
