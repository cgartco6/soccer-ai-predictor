package com.soccerai

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log
import androidx.core.app.NotificationCompat
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET

interface AIPredictionAPI {
    @GET("signals")
    suspend fun getGoldenSignals(): List<GoldenSignal>
}

data class GoldenSignal(
    val match: MatchData,
    val prediction: String,
    val confidence: Double,
    val bttsProb: Double,
    val valueEdge: Double
)

data class MatchData(
    val home_team: String,
    val away_team: String,
    val odds: Map<String, Double>
)

class PredictionService : Service() {
    private val apiService: AIPredictionAPI by lazy {
        Retrofit.Builder()
            .baseUrl("http://10.0.2.2:8000/")  // Localhost for emulator
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(AIPredictionAPI::class.java)
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val notification = NotificationCompat.Builder(this, "prediction_channel")
            .setContentTitle("SoccerAI Predictor")
            .setContentText("Monitoring for golden signals...")
            .setSmallIcon(R.drawable.ic_soccer)
            .build()

        startForeground(1, notification)

        CoroutineScope(Dispatchers.IO).launch {
            while (true) {
                try {
                    val signals = apiService.getGoldenSignals()
                    signals.filter { 
                        it.confidence > 92 && it.valueEdge > 15 
                    }.forEach { sendToTelegram(it) }
                    
                    Log.d("PredictionService", "Fetched ${signals.size} signals")
                    Thread.sleep(900000) // 15 minutes
                } catch (e: Exception) {
                    Log.e("PredictionService", "Error: ${e.message}")
                    Thread.sleep(300000) // 5 minutes on error
                }
            }
        }

        return START_STICKY
    }

    private fun sendToTelegram(signal: GoldenSignal) {
        val message = "🚨 GOLDEN SIGNAL (${signal.confidence}%)\n" +
                     "⚽ ${signal.match.home_team} vs ${signal.match.away_team}\n" +
                     "🎯 ${signal.prediction} | BTTS: ${if (signal.bttsProb > 0.65) "Yes" else "No"}\n" +
                     "💰 Value Edge: ${signal.valueEdge}%"

        val telegramIntent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, message)
            `package` = "org.telegram.messenger"
            flags = Intent.FLAG_ACTIVITY_NEW_TASK
        }
        startActivity(telegramIntent)
    }

    override fun onBind(intent: Intent): IBinder? = null
}
