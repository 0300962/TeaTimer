# TeaTimer
Push a button to remember when your tea was brewed. Simple!

Written for a Pimoroni Badger2040, with an RV3028 RTC board connected via I2C (on the QW/ST connector on the back of the Badger), and a couple of AAA batteries. 
![IMG_20221125_094712446](https://user-images.githubusercontent.com/36078310/204370054-b2c5aee0-eca0-45fe-9e20-a11258089a26.jpg)
![IMG_20221125_094810137_HDR](https://user-images.githubusercontent.com/36078310/204370913-acba5fb4-87b3-4160-8f79-70f76fcb4085.jpg)



https://user-images.githubusercontent.com/36078310/204371686-4acd3513-15dd-44d8-b518-5f3c4c7c4d70.mp4


# Notes 
1. I'm not a python programmer so sorry about that.  Basically when you press the button, the Badger detects power, enables it's onboard 3.3v regulator, updates the screen with the current time from the RTC, and then pulls it's own plug by switching off the regulator again to save the battery power. 
2. All the files should be here, check the Pimoroni examples for how to get the image (teapot.bin) into your Badger. You'll have to rename the file to main.py to get it to run on power-up.
3. You'll see a lot more in the code than just one screen; when the Badger is running on USB power, you can press the 'up' button to access the debug screens, where you can adjust the time of the external RTC board. It should handle BST automatically (without changing the RTC), your mileage may vary in other regions or if they abandon BST in the future. There IS a way to switch 12/24Hrs (using the 'a' button on the Badger) but this doesn't set it in the RTC so won't persist.
4. The teapot body took about 13.5hrs to print on an Ender-3 set to max layer height.  Support is needed; make sure to remove the internal section carefully, you'll need that space for the lever.
5. The lever just sits in the recess inside the teapot and is held in place by the Badger (the 'up' and 'down' buttons go at the top). Print this at a higher resolution and make sure your layers are running lengthways or it may snap. When you press the lever vertically it deforms slightly to press the middle button on the Badger.
6. The thing sticking out of the 'spring' is there to guide the lever (see photo), you may want to scale the spring up a couple of percent to keep the Badger more secure (or use 2 springs) depending on how your plastic behaves. You will need to snip a little off of the top of the lever so that the lid sits at a nice height once it's all printed.
