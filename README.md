# Pass things on

A web application that allows the user to donate unwanted items to trusted institutions (foundations, non-governmental organizations, local donations). The application is created by means of the Django framework, I used a user model that requires only an e-mail address and password to register. Detailed data about institutions are downloaded asynchronously using the jQuery library. Forms are handled by JavaScript.

Landing page                                      |Steps
:------------------------------------------------:|:--------------------------------------------------:
![LandingPage](https://snipboard.io/6zj7le.jpg)   |  ![LandingPage2](https://snipboard.io/PMKifR.jpg)
Organizations                                     |Add donation form
![Organizations](https://snipboard.io/y4nA9Y.jpg) |  ![AddDonation](https://snipboard.io/281jFE.jpg)
Add donation summary                              |User profile
![AddDonation2](https://snipboard.io/RvCNZ5.jpg)  |  ![PortfolioLab](https://snipboard.io/XR1JWp.jpg)

### Main functionalities:

- User profile:
    - registration
    - login
    - add donations
    - viewing past donations

- Handling the contact form (send confirmation by e-mail).
- Landing page dynamically displaying:
    - foundations
    - non-governmental organization
    - local donations
    - statistics
