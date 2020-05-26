
  // Your web app's Firebase configuration
  var firebaseConfig = {
    apiKey: "AIzaSyATwswbz2NkwjQuWE47S6nUGbIsby_xtmI",
    authDomain: "basic-8813e.firebaseapp.com",
    databaseURL: "https://basic-8813e.firebaseio.com",
    projectId: "basic-8813e",
    storageBucket: "basic-8813e.appspot.com",
    messagingSenderId: "135594414762",
    appId: "1:135594414762:web:56725af8122c8c6bf1b6d3",
    measurementId: "G-M2Z3BPN0ET"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  firebase.analytics();

  const auth = firebase.auth();
  const db = firebase.firestore();
  const functions = firebase.functions();

const starter = document.querySelector("#Starter");
const cafelist = document.querySelector("#cafe-list");
const addcafe = document.querySelector("#add-cafe-form");
const loginlist = document.querySelectorAll(".login");
const logoutlist = document.querySelectorAll(".logout");
const adminlist = document.querySelectorAll(".admin");
const details = document.querySelector(".account-details");
const adminform = document.querySelector('.admin-actions');

let html = '';
function cafename(doc,user) {
    let li = document.createElement('li');
    let name = document.createElement('span');
    let city = document.createElement('span');
    let cross = document.createElement('div');
    let write = document.createElement('div');
    let icon = document.createElement('i');

    li.setAttribute('data-id', doc.id);
    name.textContent = doc.data().name;
    city.textContent = doc.data().city;
    cross.textContent = 'x';
    icon.setAttribute("class", "fa fa-pencil");
    write.appendChild(icon);

    li.appendChild(name);
    li.appendChild(city);

    if(user.admin){
      li.appendChild(cross);
      li.appendChild(write);
    }


    cafelist.appendChild(li);

    // const li = `
    //   <li>
    //     <span> ${doc.data().name} </span>
    //     <span> ${doc.data().city} </span>
    //     <div class="write"><i class="fa fa-pencil"</i></div>
    //     <div><i class="fa fa-plus"</i></div>
    //   </li>
    // `;
    // html += li;
    //
    //  cafelist.innerHTML = html;

// deleting data
    cross.addEventListener('click', function(e) {
      e.stopPropagation();
      let id = e.target.parentElement.getAttribute('data-id');
      db.collection('cafes').doc(id).delete();

    })
// updating data
    icon.addEventListener('click',function(e) {
      e.stopPropagation();
      let id = e.target.parentElement.parentElement.getAttribute('data-id');
      let newname = prompt('Name(if not want to change click ok)');
      let newcity = prompt('City(if not want to change click ok)');

      if (newname == '' && newcity=='') {
        db.collection('cafes').doc(id).update({
          name:doc.data().name,
          city:doc.data().city
        })
        }else if (newname == '' || newcity==''){
            if (newname == '') {
              db.collection('cafes').doc(id).update({
                name:doc.data().name,
                city:newcity,
              })
            }else if (newcity == '') {
              db.collection('cafes').doc(id).update({
                name:newname,
                city:doc.data().city,
              })
            }
      }
      else {
        db.collection('cafes').doc(id).update({
          name:newname,
          city:newcity
        })
      }

    })
}

// // getting data
  // db.collection('cafes').orderBy('city').orderBy('name').get().then((snapshot) => {
  //   snapshot.docs.forEach(doc => {
  //     cafename(doc);
  //   });
  // });

// getting data according needs
// db.collection('cafes').where('city','==','Dhule').orderBy('name').get().then((snapshot) => {
//   snapshot.docs.forEach(doc => {
//     cafename(doc);
//   });
// });


//real-time getting data
// See in auth.onAuthStateChanged(user) How to real time update data;

// saving data

addcafe.addEventListener('submit', function (e){
    e.preventDefault();
    if (addcafe.name.value == '' || addcafe.city.value == '') {
      alert('Wrong Cridentals');
    }
    else{
      db.collection('cafes').add({
        name:addcafe.name.value,
        city:addcafe.city.value,
      });
    }

    addcafe.name.value = '';
    addcafe.city.value = '';
})


//#################################################

//making admin
adminform.addEventListener('submit', function(e){
  e.preventDefault();
  let admin_email = adminform['admin-email'].value;
  const adminrole = functions.httpsCallable('addAdminRole');
  adminrole({email:admin_email}).then(()=>{
    adminform.reset();
  })
})

// Tracking of User Log-in/Log-out status

auth.onAuthStateChanged(user =>{
  if(user){

    // checking whether user is admin or not
    user.getIdTokenResult().then(IdTokenResult =>{
       user.admin = IdTokenResult.claims.admin;
       console.log(user.admin);
      if(user.admin){
        adminlist.forEach(item => {
          item.style.display = 'block';
        });
      }
      else{
        adminlist.forEach(item => {
          item.style.display = 'none';
        });
      }
    })

    // showing data only for autheticated user
        loginlist.forEach(item => {
          item.style.display = 'block';
        });
        logoutlist.forEach(item => {
          item.style.display = 'none';
        });
        $('#Starter').css('visibility','visible');

    // user info
    db.collection('users').doc(user.uid).get().then((doc) => {
      let detail = `
        <h6>Welcome ${doc.data().full_name} of Age ${doc.data().age ? doc.data().age : ''}</h6>
        <h6>Logged in as ${user.email} </h6>
        <h6>You're an ${user.admin ? 'Admin':'User' }</h6>

      `;
      details.innerHTML = detail;
    })

    //real-time getting data
     db.collection('cafes').orderBy('city').orderBy('name').onSnapshot(snapshot => {
       let changes = snapshot.docChanges();

       changes.forEach(change => {
         if (change.type == 'added') {
           cafename(change.doc,user);
         }else if (change.type == 'removed') {
           let li = cafelist.querySelector('[data-id=' + change.doc.id + ']');
           cafelist.removeChild(li);
         }else if (change.type == 'modified'){
           let li = cafelist.querySelector('[data-id=' + change.doc.id + ']');
           cafelist.removeChild(li);
           cafename(change.doc);
         }
       });

     })

  }
  else{
    // showing data only for autheticated user
        adminlist.forEach(item => {
          item.style.display = 'none';
        });
        loginlist.forEach(item => {
          item.style.display = 'none';
        });
        logoutlist.forEach(item => {
          item.style.display = 'block';
        });
        $('#Starter').css('visibility','visible');
    starter.innerHTML='<h1>Log In To View List</h1>';
    details.innerHTML = '';
  }
})










// User Sign UP with Email and Password

const singup = document.querySelector('#signup-form');

singup.addEventListener('submit', function(e) {
    e.preventDefault();
    let email = singup['signup-email'].value;
    let password = singup['signup-password'].value;

    auth.createUserWithEmailAndPassword(email,password).then(cred =>{
      return db.collection('users').doc(cred.user.uid).set({
        full_name: singup['signup-fullname'].value,
        age: singup['signup-age'].value
    });
  }).then(() => {
    const modal = document.querySelector('#modal-signup');
    M.Modal.getInstance(modal).close();
    singup.reset();
    singup.querySelector('.error').innerHTML = '';
  }).catch (function (e) {
    singup.querySelector('.error').innerHTML = e.message;
  })
})


// User Sign UP with Google

const googlesignup = document.querySelector('#googlesignup');

googlesignup.addEventListener('click',function(e) {
  const base_provider = new firebase.auth.GoogleAuthProvider();

  auth.signInWithPopup(base_provider).then(function(result) {
    return db.collection('users').doc(result.user.uid).set({
      full_name: result.user.displayName,
      age: '',
  })
}).then(() => {
    const modal = document.querySelector('#modal-signup');
    M.Modal.getInstance(modal).close();
    singup.reset();
    singup.querySelector('.error').innerHTML = '';
  }).catch (function (e) {
    singup.querySelector('.error').innerHTML = e.message;
  })

})

// Logging in

const login = document.querySelector('#login-form');

login.addEventListener('submit', function(e) {
    e.preventDefault();
    let email = login['login-email'].value;
    let password = login['login-password'].value;

    auth.signInWithEmailAndPassword(email,password).then(cred =>{
      const modal = document.querySelector('#modal-login');
      M.Modal.getInstance(modal).close();
      login.reset();
      login.querySelector('.error').innerHTML = '';
    }).catch (function (e) {
      login.querySelector('.error').innerHTML = e.message;
    })

})

// Logging In Using Google
const googlelogin = document.querySelector('#googlelogin');

googlelogin.addEventListener('click',function(e) {
  const base_provider = new firebase.auth.GoogleAuthProvider();

  auth.signInWithPopup(base_provider).then(function(result) {
    const modal = document.querySelector('#modal-login');
    M.Modal.getInstance(modal).close();
    login.reset();
    login.querySelector('.error').innerHTML = '';
  }).catch (function (e) {
    login.querySelector('.error').innerHTML = e.message;
  })

})


// Logging Out From ACCOUNT

const logout = document.querySelector('#logout');
logout.addEventListener('click',function(e) {
  e.preventDefault();
  auth.signOut().then(function() {
    console.log('U have Logged Out');
  })
})
