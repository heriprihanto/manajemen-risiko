<script type="module">
  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/12.15.0/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/12.15.0/firebase-analytics.js";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyDls91HFIf1_E0X6JJ1kuE7V8I6z8tW68A",
    authDomain: "manajemen-risiko-98127.firebaseapp.com",
    projectId: "manajemen-risiko-98127",
    storageBucket: "manajemen-risiko-98127.firebasestorage.app",
    messagingSenderId: "465214376439",
    appId: "1:465214376439:web:73469cafb36d37c2b886f2",
    measurementId: "G-FLYRRYCXEX"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);
</script>