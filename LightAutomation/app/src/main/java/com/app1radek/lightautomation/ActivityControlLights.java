package com.app1radek.lightautomation;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.*;
import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;


import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

import android.util.Pair;


/**
 * Created by Radzio on 09/01/2017.
 */
public class ActivityControlLights extends Activity{

    Button btnFrom;
    Button btnUntil;
    TextView textFrom;
    TextView textUntil;
    SeekBar seekBar;
    TextView textBright;
    CheckBox boxFrom;
    CheckBox boxUntil;
    Switch switch1;
    Button btnSend;
    int brightnessLevel = 0;
    //String timeFromSend = "0000/00/00 00:00:00";
    //String timeUntilSend = "0000/00/00 00:00:00";
    String timeFromSend = "0";
    String timeUntilSend = "0";
    String lightChooser;
    int onOff =0;

    JsonRequest jsonRequest = new JsonRequest();


    //Receive data and time from ActivityTimeUntil/From
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        System.out.println("I am in OnActionResult");

        if(102 == requestCode)
        {
            System.out.println("I am in the code 102 statment");
            if(resultCode == Activity.RESULT_OK)
            {
                Bundle returnedTimeUntil = data.getExtras();
                String timeUntil = returnedTimeUntil.getString("timeDateUntil");
                timeUntilSend = timeUntil;
                textUntil.append(timeUntil);
                System.out.println("I am in Activity.RESULT_OK");
            }
        }
        else if(101 == requestCode)
        {
            System.out.println("I am in the code 101 statment");
            if(resultCode == Activity.RESULT_OK)
            {
                Bundle returnedTimeUntil = data.getExtras();
                String timeFrom = returnedTimeUntil.getString("timeDateFrom");
                timeFromSend = timeFrom;
                textFrom.append(timeFrom);
                System.out.println("I am in Activity.RESULT_OK");

            }
        }
        else if(100 == requestCode)
        {
            System.out.println("I am in the code 100 statment");
            if(resultCode == Activity.RESULT_OK)
            {
                Bundle light = data.getExtras();
                String chooseLight = light.getString("light");
                //timeFromSend = timeFrom;
                //textFrom.append(timeFrom);
                System.out.println("The Light choosen is: ------>" + chooseLight);

            }
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.control_activity);

        //seting all the components
        btnFrom = (Button)findViewById(R.id.btnFrom);
        btnUntil = (Button)findViewById(R.id.btnUntil);
        textFrom = (TextView)findViewById(R.id.textFrom);
        textUntil = (TextView)findViewById(R.id.textUntil);
        seekBar = (SeekBar)findViewById(R.id.seekBar);
        textBright = (TextView)findViewById(R.id.textBright);
        boxFrom = (CheckBox)findViewById(R.id.boxFrom);
        boxUntil = (CheckBox)findViewById(R.id.boxUntil);
        switch1 = (Switch)findViewById(R.id.switch1);
        btnSend = (Button)findViewById(R.id.btnSend);


        Intent lightData = getIntent();
        Bundle light = lightData.getExtras();
        //String chooseLight = light.getString("light");
        lightChooser = light.getString("light");
        //timeFromSend = timeFrom;
        //textFrom.append(timeFrom);
        System.out.println("The Light choosen is: ------>" + lightChooser);



        //Setting brightness of the leds
        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {

            int lightValue;
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {


                lightValue = i;
                brightnessLevel = i;


                textBright.setText("Brightness: " + i + "%  ");

            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

                textBright.setText("Brightness: " + lightValue + "%");

            }
        });

        //Check box to determine current time and date
        boxFrom.setOnClickListener(new View.OnClickListener() {
           @Override
           public void onClick(View view) {

               if(boxFrom.isChecked() == true)
               {
                   String timeStamp = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss").format(Calendar.getInstance().getTime());
                   timeFromSend = timeStamp;
                   textFrom.append(timeStamp);

               }
               else if(boxFrom.isChecked() == false)
               {
                   textFrom.clearComposingText();
                   textFrom.setText("From: ");

               }
               //textFrom.append("siema");
           }
       }
       );

        //check box to set no time specified for until time
        boxUntil.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                if(boxUntil.isChecked() == true)
                {
                    textUntil.append("Time not specified");

                }
                else if(boxFrom.isChecked() == false)
                {
                    textUntil.clearComposingText();
                    textUntil.setText("Until: ");

                }
                //textFrom.append("siema");
            }
        }
        );

        //Button from call activity which display date and time picker
        btnFrom.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(ActivityControlLights.this, ActivityTimeFrom.class);
                startActivityForResult(myIntent,101);



            }
        });

        //Button until call activity which display date and time picker
        btnUntil.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myIntent = new Intent(ActivityControlLights.this, ActivityTimeUntil.class);
                startActivityForResult(myIntent,102);



            }
        });

        //Switch to set light on or off
        switch1.setOnClickListener(new View.OnClickListener() {
        @Override
        public void onClick(View view) {

            if(switch1.isChecked() == true)
            {
                onOff = 1;
               // System.out.println("The light is ON = " + onOff );
            }
            else if(switch1.isChecked() == false)
            {
                onOff = 0;
               // System.out.println("The light is OFF = " + onOff );
            }

        }
    });

        btnSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new sendToDataBase().execute();
            }
        });

    }

    //Sends all the data to database on PI by php scripts
    class sendToDataBase extends AsyncTask<String, String,String>{





        @Override
        protected String doInBackground(String... strings) {



            //List<Pair<String,String>> params = new ArrayList<>();
            List<NameValuePair> params = new ArrayList<>();

            String bright = Integer.toString(brightnessLevel);
            String status = Integer.toString(onOff);

            //set brightness to 100 when status is On and brightness is not set
            if(onOff == 1 && brightnessLevel == 0)
                bright = "100";
            if((onOff == 0 && brightnessLevel > 0) && (timeFromSend == "0" && timeUntilSend == "0"))
                status = "1";
            if(onOff == 1 && (timeFromSend != "0" || timeUntilSend != "0"))
                status = "0";
            if((onOff == 0 && brightnessLevel == 0) && (timeFromSend != "0" || timeUntilSend != "0"))
                bright = "100";


            params.add(new BasicNameValuePair("brightness",bright));
            params.add(new BasicNameValuePair("status",status));
            params.add(new BasicNameValuePair("Time_From",timeFromSend));
            params.add(new BasicNameValuePair("Time_Until", timeUntilSend ));
            params.add(new BasicNameValuePair("light", lightChooser ));

            for(int i = 0; i<params.size(); i++)
            {
                System.out.println(params.get(i).toString());
            }



            JSONObject json = jsonRequest.makeHttpRequest("http://10.3.4.73/php/db_create.php", "POST", params);

            try {
                int success = json.getInt("success");

                if(success == 1){
                    finish();
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }


            return null;

        }
    }


}
