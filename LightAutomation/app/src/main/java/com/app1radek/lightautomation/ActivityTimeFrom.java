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
public class ActivityTimeFrom extends Activity {

    DatePicker datePicker2;
    TimePicker timePicker3;
    Button btnOk2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.set_time_from);

        datePicker2 = (DatePicker)findViewById(R.id.datePicker2);
        timePicker3 = (TimePicker)findViewById(R.id.timePicker3);

        btnOk2 = (Button)findViewById(R.id.btnOk2);

        btnOk2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                int year = datePicker2.getYear();
                int month = datePicker2.getMonth() + 1;
                int dayOfMonth = datePicker2.getDayOfMonth();

                int hours = timePicker3.getCurrentHour();
                int minute = timePicker3.getCurrentMinute();
                System.out.println("year = " + year + " month = " + month + " day = " + dayOfMonth + " hour = " + hours + " minutes = " + minute);

                //convert int to String
                String timeFrom = Integer.toString(year) + "/" + Integer.toString(month) + "/" + Integer.toString(dayOfMonth) +
                        " " + Integer.toString(hours) + ":" + Integer.toString(minute) + ":00";

                System.out.println(timeFrom);
                Intent intentChandler = getIntent();

                Bundle myBundle = new Bundle();

                myBundle.putString("timeDateFrom", timeFrom);

                intentChandler.putExtras(myBundle);

                setResult(Activity.RESULT_OK, intentChandler);

                finish();


            }
        });


    }
}