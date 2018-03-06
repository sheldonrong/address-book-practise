# Address Book Manager - Front end

Rich single page application.

### Installing

Simply run `npm install` at the current folder, wait for it to complete (pulling packages from remote server, so Internet is required).

### Development

Simply run `npm run watch`. Note at the moment, the hot patches are generated all over the place. To resolve this, you will need to eject the create-react-app package and make modification to the react-script-ts's webpack configuration file. I am stuck with deleting these hot patch files for the time being.

### Built With

* `React`
* `TypeScript`
* `Semantic UI`
* `Semantic UI - React Components`
* `Dropzone - React Component`

### Deployment

Simply run `npm run build`, compressed static files will be located in `build/static/` folder.

### Others

Due to limited time, I did not use `Redux` nor `RxJS`. Ideally both libraries are needed for enterprise level front-end applications.
And also because of this, I did not write any Jest unit tests for the front end.

### Authors
Sheldon Rong

### License
This project is licensed under the MIT License
