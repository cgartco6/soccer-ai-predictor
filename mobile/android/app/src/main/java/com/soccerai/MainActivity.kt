package com.soccerai

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.TextView

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        val startBtn: Button = findViewById(R.id.startBtn)
        val statusText: TextView = findViewById(R.id.statusText)
        
        // Start prediction service
        startBtn.setOnClickListener {
            Intent(this, PredictionService::class.java).also { intent ->
                startService(intent)
                statusText.text = "🟢 Monitoring for golden signals..."
            }
        }
    }
}
