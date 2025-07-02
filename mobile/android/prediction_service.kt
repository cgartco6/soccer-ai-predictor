package com.soccerai

import android.app.Service
import android.content.Intent
import android.os.IBinder
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class PredictionService : Service() {

    private val api = Retrofit.Builder()
        .baseUrl("https://api.soccer-ai.com/")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
        .create(AIPredictionAPI::class.java)

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Fetch signals every 15 minutes
        val timer = Timer()
        timer.scheduleAtFixedRate(object : TimerTask() {
            override fun run() {
                val signals = api.getGoldenSignals().execute().body()
                signals?.forEach { sendToTelegram(it) }
            }
        }, 0, 900000)
        
        return START_STICKY
    }
    
    private fun sendToTelegram(signal: GoldenSignal) {
        val message = "⚽ ${signal.homeTeam} vs ${signal.awayTeam}\n" +
                      "🎯 ${signal.prediction} (${signal.confidence}%)\n" +
                      "💰 Value: ${signal.valueEdge}% edge"
        
        val telegramIntent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, message)
            `package` = "org.telegram.messenger"
        }
        startActivity(telegramIntent)
    }

    override fun onBind(intent: Intent): IBinder? = null
}
