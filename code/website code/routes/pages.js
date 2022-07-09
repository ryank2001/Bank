const express = require('express');
const authController = require('/home/ubuntu-1025652/code/Controllers/auth.js');
var DomParser = require('dom-parser');
const router = express.Router();


// get requests 

router.get('/', authController.isLoggedIn, (req, res) => {
  console.log(req.user);
  if( req.user ) {  
    res.render('/home/ubuntu-1025652/code/views/profile.hbs', {
      user: req.user
    });
  } else {
    res.redirect('/login');
  }
  
});

router.get('/register', (req, res) => {
  res.render('/home/ubuntu-1025652/code/views/register.hbs');
});


router.get('/login', (req, res) => {
  res.render('/home/ubuntu-1025652/code/views/login.hbs');
});

router.get('/profile', authController.isLoggedIn, (req, res) => {
  console.log(req.user);
  if( req.user ) {  
    res.render('/home/ubuntu-1025652/code/views/profile.hbs', {
      user: req.user
    });
  } else {
    res.redirect('/login');
  }
  
});

router.get('/transactie', authController.data, (req, res) => {
  console.log("test");
  
  let dict = {};
  let counter  = 0;
  var html = ` `
  try{
    for (const element of req.user) {
      var counters = counter.toString()
      dict[counter.toString()] = element;
      counter = counter + 1;
      html += `<tr>
      <td>${dict[counters].transactie_id}</td>
      <td>${dict[counters].rekening_nummer}</td>
      <td>${dict[counters].datum}</td>
      <td>${dict[counters].hoeveelheid}</td>
      <td>${dict[counters].land}</td>
      <td>${dict[counters].bank}</td>
      <td>${dict[counters].status}</td>
      
  </tr>` }
  }
  catch{
    html = " "
  }
  
console.log(html);


  if( html != "") {
    res.render('/home/ubuntu-1025652/code/views/transactie.hbs', {
      user: html}
);
  } else {
    res.redirect('/login');
  }
  
});




module.exports = router;