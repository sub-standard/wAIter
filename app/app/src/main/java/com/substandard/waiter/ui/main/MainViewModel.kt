package com.substandard.waiter.ui.main

import androidx.lifecycle.ViewModel
import com.substandard.waiter.Drinks

class MainViewModel : ViewModel() {

    private var orderDrinks: Drinks? = null

    fun setOrder(order: Drinks) {
        orderDrinks = order
    }

    fun getOrder(): Drinks? {
        return orderDrinks
    }
}
