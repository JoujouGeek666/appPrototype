# appPrototype
## Installing the Web app as executable on the machine :
- First of all, you need to install _npm_ (Node package manager) and by extension _Node.js_ on your machine. On windows, you can install the packages From the Node.js Downloads page. To do so on MacOS/Linux, type this command in the terminal :
```
npm install -g npm
```
- Check _npm_ and _Node.js_ installations using these commands :
```
node -v
npm -v
``` 
- Install nativefier by running the below command:
```
npm install -g nativefier
```
- Go to the directory where you want to install the executable and run this command depending on your machine (Windows/Linux/MacOS):
```
nativefier --name 'Codevsi' 'https://codevsiwebapp.streamlit.app/' --platform 'windows'
```
```
nativefier --name 'Codevsi' 'https://codevsiwebapp.streamlit.app/' --platform 'linux'
```
```
nativefier --name 'Codevsi' 'https://codevsiwebapp.streamlit.app/' --platform 'mac'
```
This should create the executable in the chosen directory.
