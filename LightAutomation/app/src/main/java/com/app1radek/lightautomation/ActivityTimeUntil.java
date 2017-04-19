package com.app1radek.lightautomation;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.TimePicker;

/**
 * Created by Radzio on 09/01/2017.
 */
public class ActivityTimeUntil extends Activity {

    DatePicker datePicker;
    TimePicker timePicker;
    Button btnOk;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.set_time_until);

        datePicker = (DatePicker)findViewById(R.id.datePicker);
        timePicker = (TimePicker)findViewById(R.id.timePicker2);

        btnOk = (Button)findViewById(R.id.btnOk);


        btnOk.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                int year = datePicker.getYear();
                int month = datePicker.getMonth() + 1;
                int dayOfMonth = datePicker.getDayOfMonth();

                int hours = timePicker.getCurrentHour();
                int minute = timePicker.getCurrentMinute();
                System.out.println("year = " + year + " month = " + month + " day = " + dayOfMonth + " hour = " + hours + " minutes = " + minute);

                //convert int to String
                String timeUntil = Integer.toString(year) + "/" + Integer.toString(month) + "/" + Integer.toString(dayOfMonth) +
                        " " + Integer.toString(hours) + ":" + Integer.toString(minute) + ":00";

                System.out.println(timeUntil);
                Intent intentChandler = getIntent();

                Bundle myBundle = new Bundle();

                myBundle.putString("timeDateUntil", timeUntil);

                intentChandler.putExtras(myBundle);

                setResult(Activity.RESULT_OK, intentChandler);

                finish();


            }
        });


    }
}
