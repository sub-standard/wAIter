package com.substandard.waiter.ui.main

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProviders
import androidx.navigation.NavController
import androidx.navigation.findNavController
import com.substandard.waiter.Drinks
import com.substandard.waiter.R
import com.substandard.waiter.databinding.OrderFragmentBinding

class OrderFragment : Fragment() {
    private lateinit var viewModel: MainViewModel

    private lateinit var navController: NavController

    private lateinit var binding: OrderFragmentBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding= OrderFragmentBinding.inflate(inflater, container, false)
        binding.lifecycleOwner = this
        return binding.root

    }

    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)
        viewModel = ViewModelProviders.of(activity!!).get(MainViewModel::class.java)
        binding.fragment = this
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        navController = view.findNavController()
    }

    fun onDrinkPress(drink: Drinks) {
        viewModel.setOrder(drink)
        viewModel.createOrder()


        //TODO send signal to site with drink

        navController.navigate(R.id.action_order_fragment_to_orderedFragment)

    }
}
