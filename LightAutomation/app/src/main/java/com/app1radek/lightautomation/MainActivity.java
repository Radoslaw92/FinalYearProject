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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        l1 = (Button)findViewById(R.id.l1);
        l2 = (Button)findViewById(R.id.l2);
        l3 = (Button)findViewById(R.id.l3);

        l1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(MainActivity.this, ActivityControlLights.class);
                Bundle myData = new Bundle();
                myData.putString("light", "light1");
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
                myData.putString("light", "light2");
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
                myData.putString("light", "light3");
                myIntent.putExtras(myData);
                //startActivityForResult(myIntent,100);
                startActivity(myIntent);

            }
        });


    }
}
