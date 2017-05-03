package com.app1radek.lightautomation;

import android.app.Activity;
import android.app.Instrumentation;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends Activity {

    Button l1;
    Button l2;
    Button l3;
    Button l4;
    Button l5;
    Button l6;
    Button l7;
    Button l8;
    Button l9;
    Button l10;
    Button l11;
    Button l12;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        l1 = (Button)findViewById(R.id.l1);
        l2 = (Button)findViewById(R.id.l2);
        l3 = (Button)findViewById(R.id.l3);
        l4 = (Button)findViewById(R.id.l4);
        l5 = (Button)findViewById(R.id.l5);
        l6 = (Button)findViewById(R.id.l6);
        l7 = (Button)findViewById(R.id.l7);
        l8 = (Button)findViewById(R.id.l8);
        l9 = (Button)findViewById(R.id.l9);
        l10 = (Button)findViewById(R.id.l10);
        l11 = (Button)findViewById(R.id.l11);
        l12 = (Button)findViewById(R.id.l12);


        l1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(MainActivity.this, ActivityControlLights.class);
                Bundle myData = new Bundle();
                myData.putString("light", "light_1");
                myIntent.putExtras(myData);
                //startActivityForResult(myIntent,100);
                startActivity(myIntent);

            }
        });
        l2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(MainActivity.this, ActivityControlLights.class);
                Bundle myData = new Bundle();
                myData.putString("light", "light_2");
                myIntent.putExtras(myData);
                //startActivityForResult(myIntent,100);
                startActivity(myIntent);

            }
        });

        l3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(MainActivity.this, ActivityControlLights.class);
                Bundle myData = new Bundle();
                myData.putString("light", "light_3");
                myIntent.putExtras(myData);
                startActivity(myIntent);

            }
        });
        l4.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(MainActivity.this, ActivityControlLights.class);
                Bundle myData = new Bundle();
                myData.putString("light", "light_4");
                myIntent.putExtras(myData);
                startActivity(myIntent);

            }
        });

        l5.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(MainActivity.this, ActivityControlLights.class);
                Bundle myData = new Bundle();
                myData.putString("light", "light_5");
                myIntent.putExtras(myData);
                startActivity(myIntent);

            }
        });

        l6.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(MainActivity.this, ActivityControlLights.class);
                Bundle myData = new Bundle();
                myData.putString("light", "light_6");
                myIntent.putExtras(myData);
                startActivity(myIntent);

            }
        });

        l7.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(MainActivity.this, ActivityControlLights.class);
                Bundle myData = new Bundle();
                myData.putString("light", "light_7");
                myIntent.putExtras(myData);
                startActivity(myIntent);

            }
        });

        l8.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(MainActivity.this, ActivityControlLights.class);
                Bundle myData = new Bundle();
                myData.putString("light", "light_8");
                myIntent.putExtras(myData);
                startActivity(myIntent);

            }
        });

        l9.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(MainActivity.this, ActivityControlLights.class);
                Bundle myData = new Bundle();
                myData.putString("light", "light_9");
                myIntent.putExtras(myData);
                startActivity(myIntent);

            }
        });

        l10.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(MainActivity.this, ActivityControlLights.class);
                Bundle myData = new Bundle();
                myData.putString("light", "light_10");
                myIntent.putExtras(myData);
                startActivity(myIntent);

            }
        });

        l11.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(MainActivity.this, ActivityControlLights.class);
                Bundle myData = new Bundle();
                myData.putString("light", "light_11");
                myIntent.putExtras(myData);
                startActivity(myIntent);

            }
        });

        l12.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(MainActivity.this, ActivityControlLights.class);
                Bundle myData = new Bundle();
                myData.putString("light", "light_12");
                myIntent.putExtras(myData);
                startActivity(myIntent);

            }
        });



    }
}
