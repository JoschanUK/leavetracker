# Introduction
Leave Tracking System is a programme which automatic and help the organisation to keep track of the staff annual leave and sick leave.
They system is able to create new record according to job grade, create new annual leave, email the outstanding balance to staff and is able to delete the record when the staff leave the organisation. It is a system that is linked to a google sheet which keeps track of the information. 

![alt text](<images/main screen.jpg>) [alt text](README.md)

# Features

In this section, we shows the users what to expect and what features are presented in this programme.

**Navigation options**

There are a total of 8 options which user can select from. The options are :

1. Create New Staff Record
2. Take Leave
3. Email Details
4. Display All Staff Details
5. Display Staff Leave Record
6. Clear Screen
7. Delete Staff Record
8. Exit System

**option <1> - Create New Staff Record**

Option <1> is used to create a new staff record. The programme will :
    
    - The user is aksed to input the job grade [A, B, C, D].
    - Enter First Name, Last Name and email address.
    - The system will based on user input of the job grade and assign the number of leave to the record. 
    - The system will also assign a new staff number.
    - Job Grade and the Allocated Annual Leave is found in the google sheet under the worksheet tab grade.
    - These information collected is then saved in the google sheet under the worksheet tab staff_details.

**option <2> - Take Leave**

Option <2> is used to keep track of leave taken by the staffs in the organisation. The programme will :
    
    - The programme will first display the list of staffs found in the google sheet under the worksheet tab staff_details.
    - User is to input the staff number who is going to take an annual leave. 
    - After which, the start date and end date is to be entered by the user.
    - The programme will then display the reason for taking the annual leave. The reasons are holidays/time off, sickness, childcare and others. These reasons are extracted from the google sheet under the worksheet tab reason.
    - Once the user has entered the reason. A new record will be created with all these information and stored in the google sheet under the worksheet tab records.
    - If user selected, holidays/time off or sickness reasons. The system will update the worksheet tab staff_details to deduct the annual leave for holidays/ time off and to add the number of days taken for sickness reason.

![alt text](images/takeleave.jpg)   


**option <3> - Email Details**

Option <3> is to email the staff the latest total annual leave and the number of sick leave taken. The programme will :
    
    - The programme will first display the list of staffs found in the google sheet under the worksheet tab staff_details.
    - User is to input the staff number so that the system and generate an email and send to the user email address which is stored in the google sheet under the worksheet tab staff_details.

![alt text](images/Email.jpg)


**option <4> - Display All Staff Details**

Option <4> is an option to display all the staff details in the organisation. The information is taken from the google sheet under the worksheet tab staff_details.

![alt text](images/display_allstaff.jpg)


**option <5> - Display Staff Leave Record**

Option <5> is to display all the leave record of a particular staff. The programme will :

    - The programme will first display the list of staffs found in the google sheet under the worksheet tab staff_details.
    - User is to input the staff number so that the system will retrieve all the records from the google sheet under the worksheet tab records.
    - The system will then display all the leave details taken by the selected staff.

![alt text](images/display_selectstaff.jpg)

![alt text](images/display_selectstaff_records.jpg)


**option <6> - Clear Screen**

Option <6> is just to clear the screen.

![alt text](images/clearscreen.jpg)


**option <7> - Delete Staff Record**

Option <7> is to delete a slected staff record. The programme will:

    - The programme will first display the list of staffs found in the google sheet under the worksheet tab staff_details.
    - User is to input the staff number which they want to delete.
    - Once selected, the system will remove that particular staff record from the google sheet under the worksheet tab staff_details.

![alt text](images/delete.jpg)    


**option <00> - Exit System**

Option <00> is to end the programme.

# Python Features implemented in this programme.

1. Change of colour and bolding the text in the main screen.
2. Retrieving information from a tab in a google sheet.
3. Update and append new record into a google sheet.
4. Delete a record in a google sheet.
5. Updating a particular cell in a google sheet.
6. Sending an email.

# Features left to implement

- To manually update a particular cell in the google sheet


# Testing

**Validator Testing**

- HTML
  - No errors were returned when passing through the official [W3C validator](https://validator.w3.org)

  | Link| Result |
  | --- | ---|
  |https://joschanuk.github.io/love-dogs/index.html | No Error |
  |https://joschanuk.github.io/love-dogs/gallery.html | No Error |
  |https://joschanuk.github.io/love-dogs/caring.html | No Error |
  |https://joschanuk.github.io/love-dogs/contact.html | No Error |

- CSS
  - No errors were found when passing through the official [(Jigsaw) validator](https://jigsaw.w3.org/css-validator/)

- Web Pages Testing

    | Test | Expectation | How to carry out | Result |
    | ---  | --- | ---| ---|
    | Nav bar | To be able to bring you to another webpage | By clicking on the text|Pass|
    | Dog walk sign up | User details are captured | Enter sign up details | Pass|
    | Social Media | Re direct to the website log in page | Click on the icons | Pass|
    | Audio| The audio is played | Clicking on the play button | Pass|
    | Video | The video is played| Clicking on the Play button| Pass|
    | Map | The Map will be enlarged | Clicking on the map | Pass|
    | Resizing on different devices | The layout is correct | Using the inspect code | Pass|
    | Deploy Website | Website is working and usable | Deploy from Github| Pass|

# Deployment

The site was deployed to GitHub pages. The steps to deploy are as follows:

1. On GitHub, navigate to your site's repository.
2. Under your repository name, click  Settings. If you cannot see the "Settings" tab, select the  dropdown menu, then click Settings.
3. Screenshot of a repository header showing the tabs. The "Settings" tab is highlighted by a dark orange outline.
4. In the "Code and automation" section of the sidebar, click  Pages.
5. Under "Build and deployment", under "Source", select Deploy from a branch.
6. Under "Build and deployment", use the branch dropdown menu and select a publishing source.
Screenshot of Pages settings in a GitHub repository. A menu to select a branch for a publishing source, labeled "None," is outlined in dark orange.
7. Click Save.

Once the master branch has been selected, the page will be automatically refreshed with a detailed ribbon display to indicate the successful deployment.

The live link can be found here - https://joschanuk.github.io/love-dogs/

# Credits

**Content and Media**

- The icons in the footer were taken from [Font Awesome](https://fontawesome.com/).
- External links are taken from RSPCA, Battersea and Dogs Trust.
- Source codes from Love Running to build my Sign up for dog walk form and the four social media icons.
- Downloaded a mp3 and mp4 (music and video) from Youtube.
- [W3school](https://www.w3schools.com) - For guiding me how to write the codes.
- Text in the caring page is taken from website [Animal Foundation.com](https://animalfoundation.com/whats-going-on/blog/basic-necessities-proper-pet-care).
- All walker's pictures are taken from my personal photo album.
- Instruction to deploy is taken from [Github](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
- Putting google maps using iframe [stackoverflow](https://stackoverflow.com/questions/23737427/how-to-put-two-iframes-side-by-side).
- Pure CSS Hamburger [fold-out menu](https://codepen.io/erikterwan/pen/EVzeRP). 