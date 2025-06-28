class PredictionService : Service() {
    private val aiBinder = LocalBinder()
    private val predictionClient = Retrofit.Builder()
        .baseUrl("https://api.soccer-ai.com/")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
        .create(AIPredictionAPI::class.java)

    inner class LocalBinder : Binder() {
        fun getService(): PredictionService = this@PredictionService
    }

    override fun onBind(intent: Intent): IBinder = aiBinder

    fun getGoldenSignals(callback: (List<GoldenSignal>) -> Unit) {
        predictionClient.getSignals().enqueue(object : Callback<List<GoldenSignal>> {
            override fun onResponse(
                call: Call<List<GoldenSignal>>,
                response: Response<List<GoldenSignal>>
            ) {
                if (response.isSuccessful) {
                    response.body()?.let { signals ->
                        // Filter for high-confidence signals
                        val golden = signals.filter { 
                            it.confidence > 92 && it.valueEdge > 15 
                        }
                        callback(golden)
                    }
                }
            }

            override fun onFailure(call: Call<List<GoldenSignal>>, t: Throwable) {
                Log.e("PredictionService", "API call failed", t)
            }
        })
    }

    fun sendToTelegram(signal: GoldenSignal) {
        val telegramIntent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, formatSignal(signal))
            package = "org.telegram.messenger"
        }
        startActivity(telegramIntent)
    }

    private fun formatSignal(signal: GoldenSignal): String {
        return "⚽ ${signal.homeTeam} vs ${signal.awayTeam}\n" +
               "🎯 ${signal.prediction} (${signal.confidence}% confidence)\n" +
               "💰 Value: ${signal.valueEdge}% edge\n" +
               "⏰ ${signal.matchTime}"
    }
}
