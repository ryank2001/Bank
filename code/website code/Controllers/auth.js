const mysql = require("mysql2");
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const { promisify } = require('util');
const async = require("hbs/lib/async");


//  connectie met de database word gemaakt.
const db = mysql.createConnection({
  host: '127.0.0.1',
  user: 'root',
  password: '',
  database: 'baov'
})


exports.login = async (req, res) => {
    try {
      const { email, password } = req.body;
      // Als er geen wachtwoord of email ingevoerd word krijgt de gebruiker een warning message te zien.
      if( !email || !password ) {
        return res.status(400).render('/home/ubuntu-1025652/code/views/login.hbs', {
          message: 'Voer alstublieft een email en wachtwoord in'
        })
      }

      
      // Een sql query en code om te kijken of het wachtwoord wat de gebruiker ingevoerd heeft klopt met het wachtwoord van de database.
      db.query('SELECT * FROM user_detail WHERE email = ?', [email], async (error, results) => {
        console.log(await results);
        if(results[0] == undefined){
          return res.status(400).render('/home/ubuntu-1025652/code/views/login.hbs', {
            message: 'Email of wachtwoord is onjuist'
          })
        }

        if( !results || !(await bcrypt.compare(password, await results[0].password)) ) {
          res.status(401).render('/home/ubuntu-1025652/code/views/login.hbs', {
            message: 'Email of wachtwoord is onjuist'
          })
        // Als het wachtwoord klopt word er een cookie aangemaakt zodat de gebruiker niet heletijd hoeft in te loggen.
        } else {
          const id = results[0].user_id;
          
  
          const token = jwt.sign({ id }, process.env.JWT_SECRET, {
            expiresIn: process.env.JWT_EXPIRES_IN
          });
  
          console.log("The token is: " + token);
          // Na hoeveel seconden de cookie expired.
          const cookieOptions = {
            expires: new Date(
              Date.now() + process.env.JWT_COOKIE_EXPIRES * 24 * 60 * 60 * 1000
            ),
            httpOnly: true
          }
          // Gebruiker word ingelogd.
          res.cookie('jwt', token, cookieOptions );
          res.status(200).redirect("/profile");
        }
  
      })
  
    } catch (error) {
      console.log(error);
    }
  }

  
exports.register = (req, res) => {
    console.log(req.body);
    
    const { user_id, voornaam, achternaam, email, geboorte_datum, password } = req.body;
    // SQL query om te kijken of de e-mail al in gebruik is, zoja krijgt de gebruiker een warning message.
    db.query('SELECT email FROM user_detail WHERE email = ?', [email], async (error, results) => {
      if(error) {
        console.log(error);
      }
  
      if( results.length > 0 ) {
        return res.render('/home/ubuntu-1025652/code/views/register.hbs', {
          message: 'Email is al in gebruik'
        })
      }
      
      let hashedPassword = await bcrypt.hash(password, 8);
      console.log(hashedPassword);
      // SQL query om de nieuwe gebruiker in de database te zetten met een hashed password.
      db.query('INSERT INTO user_detail SET ?', {user_id: user_id, voornaam: voornaam, achternaam: achternaam, email: email, geboorte_datum: geboorte_datum, password: hashedPassword}, (error, results) => {
        if(error) {
          console.log(error);
        } else {
          console.log(results);
          return res.render('/home/ubuntu-1025652/code/views/register.hbs', {
            message: 'Gebruiker is aangemaakt'
          });
        }
        res.redirect("/login");
      })
    });
  }

exports.isLoggedIn = async (req, res, next) => {
    // console.log(req.cookies);
    if(req.cookies.jwt) {
      try {
        //Bekijken of de token nog  geldig is
        const decoded = await promisify(jwt.verify)(req.cookies.jwt,
        process.env.JWT_SECRET
        );
  
        console.log(decoded);
  
        // SQL query om te bekijken of de gebruiker nog bestaat
        db.query('SELECT * FROM user_detail WHERE user_id = ?', [decoded.id], (error, result) => {
          console.log(result);

          if(!result) {
            return next();
          }
  
          req.user = result[0];
          console.log("User is")
          console.log(req.user);
          return next();
  
        });
      } catch (error) {
        console.log(error);
        return next();
      } 
    } else {
      next();
    }
  }

exports.testt = async (req, res, next) => {
    // console.log(req.cookies);
    if(req.cookies.jwt) {
      try {
        //Bekijken of de token nog  geldig is
        const decoded = await promisify(jwt.verify)(req.cookies.jwt,
        process.env.JWT_SECRET
        );
  
        console.log(decoded);
  
        // SQL query om te bekijken of de gebruiker nog bestaat
        db.query('SELECT * FROM user_detail WHERE user_id = ?', [decoded.id], (error, result) => {
          console.log(result);
  
          if(!result) {
            return next();
          }
  
          req.user = result[0];
          console.log("User is")
          console.log(req.user);
          return next();
  
        });
      } catch (error) {
        console.log(error);
        return next();
      } 
    } else {
      next();
    }
  }



// Gebruiker uitloggen en de cookie laten expiren.
exports.logout = async (req, res) => {
    res.cookie('jwt', 'logout', {
      expires: new Date(Date.now() + 2*1000),
      httpOnly: true
    });
    // Terug naar de login page gaan
    res.status(200).redirect('/login');
  }


exports.data = async (req, res, next) => {
    // console.log(req.cookies);
    if(req.cookies.jwt) {
      try {
         //Bekijken of de token nog  geldig is
        const decoded = await promisify(jwt.verify)(req.cookies.jwt,
        process.env.JWT_SECRET
        );
  
        console.log(decoded);
          
        //SQL Query om te selecteren welke useer zijn transactie geschiedenis word gebruikt.
        db.query('SELECT * FROM rekening WHERE user_id = ?', [decoded.id], async(error, result) => {
          console.log(result);
  
          try{
            result = result[0].rekening_nummer
          }
          catch{
            req.user = ""
            return next()
          }

          //SQL query om te selecteren welke transactie geschiedenis word gebruikt.
          let myPromise = new Promise(function(resolve) {

            sql = 
            db.query('SELECT * FROM transactie WHERE rekening_nummer = ?', [result], function(err, result) {
              
                if(!result) {
                return next();
                }
              
                if (err){
                  console.log(err);
                  resolve(0);
                }
              
                if (result[0] == undefined){
                    resolve(undefined);
                }
                  resolve(result);

              });
          });
          
      
       
          await myPromise
          req.user = await myPromise;
          console.log("User is")
          console.log( await myPromise);
          return next();
           });
      
      } catch (error) {
        console.log(error);
        return next();
      } 
    } else {
      next();
    }
  }  
  