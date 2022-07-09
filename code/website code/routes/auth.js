const express = require('express');
const authController = require('/home/ubuntu-1025652/code/Controllers/auth.js');

const router = express.Router();

// post requests 
router.post('/register', authController.register );

router.post('/login', authController.login );

router.get('/logout', authController.logout );


module.exports = router;
