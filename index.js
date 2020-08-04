// index.js
require('dotenv').config()
const Mustache = require('mustache');
const fs = require('fs');
const request = require('request');
const MUSTACHE_MAIN_DIR = './view/main.mustache';
/**
  * DATA is the object that contains all
  * the data to be provided to Mustache
  * Notice the "name" and "date" property.
*/
let DATA = {
    name: 'Jean-Loup',
    nasa_img: null,
};

request(`https://api.nasa.gov/planetary/apod?api_key=${process.env.NASA_API_KEY}`, { json: true }, (err, res, body) => {
    if (err) { return console.log(err); }
    console.log(body.url);
    console.log(body.explanation);
    console.log(body);
    DATA.nasa_img = body.hdurl;
    DATA.img_explanation = body.explanation;
    DATA.img_explanation = body.explanation;
    DATA.img_title = body.title;
    generateReadMe();
});

function generateReadMe() {
    fs.readFile(MUSTACHE_MAIN_DIR, (err, data) => {
        if (err) throw err;
        const output = Mustache.render(data.toString(), DATA);
        fs.writeFileSync('README.md', output);
    });
}
