using System;
using System.Collections;
using UnityEngine;

public class light_2 : MonoBehaviour
{

    public int numBrightness;
    public int lightStatus;
    public string lightID = "light_2";

    void Start()
    {

        StartCoroutine(queryDb());
    }

    //scan if key has been pressed 
    void Update()
    {

        if (Input.GetKeyUp(KeyCode.Alpha2))
        {
            if (numBrightness > 0 && lightStatus == 1)
            {

                sendDb("0", "0");
            }
            else if (numBrightness == 0 && lightStatus == 0)
            {
                sendDb("100", "1");
            }

        }
    }

    //send id to php script and query right column id db. receive value for brightness and status of light. turn light ON/OFF 
    //depending of the light staus. Repeat function every second
    IEnumerator queryDb()
    {
        char splitChar = '|';
        string[] values;
        while (true)
        {
            WWWForm form = new WWWForm();
            form.AddField("light", lightID);
            WWW getLight = new WWW("http://10.3.4.73/php/unity/db_create.php", form);
            yield return getLight;
            string lightsData = getLight.text;
            values = lightsData.Split(splitChar);
            yield return new WaitForSeconds(1);

            numBrightness = Int32.Parse(values[0]);
            lightStatus = Int32.Parse(values[1]);

            if (numBrightness > 0 && lightStatus == 1)
                this.GetComponent<Light>().enabled = true;
            else
                this.GetComponent<Light>().enabled = false;

        }
    }

    //Send to database new status when button is pressed in unity. Send status, brightness and ID of the light.
    public void sendDb(String bright, String lightStatus)
    {
        WWWForm form = new WWWForm();
        form.AddField("brightness", bright);
        form.AddField("status", lightStatus);
        form.AddField("light", lightID);
        WWW www = new WWW("http://10.3.4.73/php/unity/updateFromUnity.php", form);
    }
}
