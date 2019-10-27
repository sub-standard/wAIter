package com.substandard.waiter.ui.main

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import androidx.navigation.NavController
import androidx.navigation.findNavController
import com.substandard.waiter.databinding.DeliveryFragmentBinding

class DeliveryFragment : Fragment() {
    private lateinit var viewModel: MainViewModel

    private lateinit var binding: DeliveryFragmentBinding

    private lateinit var navController: NavController

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = DeliveryFragmentBinding.inflate(inflater, container, false)
        binding.lifecycleOwner = this
        return binding.root
    }

    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)
        viewModel = ViewModelProviders.of(this).get(MainViewModel::class.java)
        binding.fragment = this
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        navController = view.findNavController()

        viewModel.status.observe(this, Observer {
            if (it == "delivered") {
                Toast.makeText(activity!!, "Enjoy your drink!", Toast.LENGTH_LONG).show()
                navController.popBackStack()
            }
        })
    }

    fun onDeliveredPress() {
        viewModel.orderDelivered()
    }
}
