$(".navbar-toggler").click(function (event) {
      $(".navbar-collapse").collapse('show');
});

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
