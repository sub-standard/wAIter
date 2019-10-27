package com.substandard.waiter.ui.main

import android.util.Log
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope

import com.substandard.waiter.Drinks
import com.substandard.waiter.MongoClient
import com.uriio.beacons.model.iBeacon
import kotlinx.coroutines.*
import kotlinx.coroutines.Dispatchers.IO
import org.bson.types.ObjectId

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

    // send a signal to database
    fun createOrder() {
        mongo.client.callFunction<String>(
            "new_order"
            , listOf(when(orderDrinks) {
                Drinks.SOTB -> "Sex on the Beach"
                Drinks.AS -> "Aperol Spritz"
                Drinks.BL -> "Blue Lagoon"
                Drinks.BM -> "Bloody Mary"
                Drinks.MJ -> "Mojito"
                Drinks.MT -> "Mai Tai"
                Drinks.PR -> "Purple Rain"
                Drinks.WM -> "Watermelon Margarita"
                else -> null
            }), String::class.java
        )
            .addOnCompleteListener {
                orderId = it.result
                viewModelScope.launch {
                    pollOrder()
                }
            }

    }

    fun checkOrder() {
        mongo.client.callFunction<String>(
            "get_order_status"
            , listOf(ObjectId(orderId)), String::class.java
        )
            .addOnCompleteListener {
                _status.postValue(it.result)
                Log.d("status", it.result)
            }
    }

    suspend fun pollOrder() = Dispatchers.IO {
        while (status.value != "sending") {
            delay(2000)
            checkOrder()
        }
    }
}