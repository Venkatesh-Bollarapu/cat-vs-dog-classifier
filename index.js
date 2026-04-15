const express = require('express');
const multer = require('multer');
const {spawn} = require('child_process');
const upload = multer({ dest: 'uploads/' });
const app = express();
app.get('/',(req,res)=>{
    res.sendFile(__dirname + '/input.html');
});
app.post('/upload', upload.single('image'), (req, res) => {
    const python = spawn('python3', ['project1.py', req.file.path]);
    python.stdout.on('data', (data) => {
        res.send(data.toString());  // send immediately upon receiving data
    });

    python.stderr.on('data', (data) => {
        res.send(data.toString()); 
    });
});

app.listen(3000,()=>
{
    console.log('Server is running on port 3000');
})

