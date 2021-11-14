function checklogin(){
    firebase.auth().onAuthStateChanged(function(user) {
        if (user) {
    
          var user = firebase.auth().currentUser;
          if(user != null){
              location.replace(window.location.href+'/home');
              console.log(window.location.href+'/home');
           }
           else{
                location.replace(window.location.href+'/index');
                console.log(window.location.href+'/index');
           }
        }
    });
}

function logout(){
firebase.auth().signOut().then(()=>{
  location.replace(window.location.href+'/index');
 })
}