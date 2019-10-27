package com.substandard.waiter.ui.main

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import androidx.navigation.NavController
import androidx.navigation.findNavController
import com.substandard.waiter.Drinks
import com.substandard.waiter.R
import com.substandard.waiter.databinding.OrderedFragmentBinding
import kotlinx.android.synthetic.main.ordered_fragment.*

class OrderedFragment : Fragment() {
    private lateinit var viewModel: MainViewModel

    private lateinit var navController: NavController

    private lateinit var binding: OrderedFragmentBinding


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = OrderedFragmentBinding.inflate(inflater, container, false)
        binding.lifecycleOwner = this

        return binding.root

    }

    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)
        viewModel = ViewModelProviders.of(activity!!).get(MainViewModel::class.java)
        binding.viewModel = viewModel

        // Change image based on drink ordered
        when (viewModel.getOrder()) {
            Drinks.SOTB -> drinkOrdered.setImageResource(R.drawable.sex_on_the_beach)
            Drinks.AS -> drinkOrdered.setImageResource(R.drawable.aperol_spritz)
            Drinks.BL -> drinkOrdered.setImageResource(R.drawable.blue_lagoon)
            Drinks.BM -> drinkOrdered.setImageResource(R.drawable.bloody_mary)
            Drinks.MJ -> drinkOrdered.setImageResource(R.drawable.mojito)
            Drinks.MT -> drinkOrdered.setImageResource(R.drawable.mai_tai)
            Drinks.PR -> drinkOrdered.setImageResource(R.drawable.purple_rain)
            Drinks.WM -> drinkOrdered.setImageResource(R.drawable.watermelon_margarhitas)
        }

        viewModel.startBeacon()


        viewModel.status.observe(this, Observer {
            if (it == "sending") {
                navController.navigate(R.id.action_ordered_fragment_to_delivery_fragment)
            }
        })
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        navController = view.findNavController()

    }
}
