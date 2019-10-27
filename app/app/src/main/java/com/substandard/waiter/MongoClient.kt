package com.substandard.waiter

import com.mongodb.stitch.android.core.Stitch
import com.mongodb.stitch.core.auth.providers.anonymous.AnonymousCredential

class MongoClient {
    val client = Stitch.getDefaultAppClient()

    init {
        client.auth.loginWithCredential(AnonymousCredential())
    }
}
