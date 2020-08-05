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
let data = {
    name: 'Jean-Loup',
    nasa_img: null,
};

request(`https://api.nasa.gov/planetary/apod?api_key=${process.env.NASA_API_KEY}`, { json: true }, (err, res, body) => {
    if (err) { return console.log(err); }
    data.nasa_img = body.hdurl === undefined ? body.url : body.hdurl;
    data.img_explanation = body.explanation;
    data.img_title = body.title;
    data.is_video = body.media_type === "video"
    console.log(body)
    generateReadMe();
});

function generateReadMe() {
    fs.readFile(MUSTACHE_MAIN_DIR, (err, file) => {
        if (err) throw err;
        const output = Mustache.render(file.toString(), data);
        fs.writeFileSync('README.md', output);
    });
}
