// index.js
require('dotenv').config()
const Mustache = require('mustache');
const fs = require('fs');
const request = require('request');
const MUSTACHE_MAIN_DIR = './view/main.mustache';

let data = {
    name: 'Jean-Loup',
    nasa_img: null,
};

request(`https://api.nasa.gov/planetary/apod?api_key=${process.env.NASA_API_KEY}`, { json: true }, (err, res, body) => {
    if (err) { return console.log(err); }
    if (!body) { return console.log(res); }
    data.nasa_img =  body.url;
    data.img_explanation = body.explanation;
    data.img_title = body.title;
    data.is_video = body.media_type === "video"
    if (data.is_video) {
        data.video_id = youtube_parser(body.url)
    }
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


function youtube_parser(url) {
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match = url.match(regExp);
    return (match && match[7].length == 11) ? match[7] : false;
}