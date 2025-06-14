# FRESH FUTURES

#### Caption
<img src="" alt=""/>

## Description
Brief description. 

## Quick Links
* **Project planning** can be found [here](add link).
* **Wireframe** can be found [here](add link).
* **GitHub repo** can be found [here](https://github.com/annamiriams/fresh-futures).
* **Deployed project** link can be found [here](add link).

## Table of Contents
* [Technologies Used](#technologiesused)
* [Features](#features)
* [Design](#design)
* [Project Next Steps](#nextsteps)
* [About the Author](#author)
* [Works Cited](#workscited)

## <a name="technologiesused"></a>Technologies Used
* (ie JavaScript, HTML, CSS, etc.)
* 
* 

## <a name="design"></a>Design
* Notable design details including what inspired the design.

## <a name="nextsteps"></a>Project Next Steps
* 
* 
* 

## <a name="author"></a>About The Authors
* Name, role: [LinkedIn](add link)
* Name, role: [LinkedIn](add link)
* Name, role: [LinkedIn](add link)
* Name, role: [LinkedIn](add link)
* Name, role: [LinkedIn](add link)

## <a name="workscited"></a>Works Cited:
* **[AbstractUser](https://medium.com/@engr.tanveersultan53/when-and-how-to-use-django-abstractuser-and-abstractbaseuser-f02922745431)**: Used to simplify User Model by accessing Django's default fields (like username, first_name, last_name, etc).
* **[Django Field "choices"](https://vindevs.com/blog/how-to-use-django-field-choices-with-code-examples-p60/#:~:text=The%20choices%20option%20in%20a,forms%20and%20the%20Django%20admin.)**: Learning about "options" in Django was particularly when handling the user survey on the backend. The [docs](https://docs.djangoproject.com/en/5.2/ref/models/fields/) were also a great resource.
* **[Hamburger fold-out menu](https://codepen.io/erikterwan/pen/EVzeRP)**: A guide on creating a fold-out hamburger menu using pure CSS.
* **[Django Data Migrations](https://vindevs.com/blog/how-to-write-a-django-data-migration-how-they-work-p76/)**: In the user survey, a user needs to have the ability to "select all [checkboxes] that apply". Since the corresponding models were ManyToMany relaetionships, we needed to write a data migration to provide the various checkbox options. Thanks to an initial prompt in chatGPT that led us down a rabbit hole about data migrations and many other resources (including [this one](https://djangocentral.com/creating-an-empty-migration-file-in-django/), and of course [the docs](https://docs.djangoproject.com/en/5.2/howto/writing-migrations/)), we were able to render multi-select options for the user.
* **[reverse_lazy](https://stackoverflow.com/questions/48669514/difference-between-reverse-and-reverse-lazy-in-django)**: While working out the flow between surveys, we needed to use reverse_lazy instead of reverse so that the success_url wasn't generated immediately. 
* **[CSS: fade in](https://dev.to/tiaeastwood/super-simple-css-animation-for-fade-in-on-page-load-2p8m)**: At this point in time, we have the BeetBot icon on the app, however it isn't functional. To show a message noting the "feature is coming soon", we used this quick guide for using keyframes to create the fade in animation of the message.
* **[enter name of method/theory/etc](link)**: Description of how this resource was utilized.
* **[enter name of method/theory/etc](link)**: Description of how this resource was utilized.
* **[enter name of method/theory/etc](link)**: Description of how this resource was utilized.
