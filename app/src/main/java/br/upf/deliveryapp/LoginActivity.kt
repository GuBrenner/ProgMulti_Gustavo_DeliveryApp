package br.upf.deliveryapp

import android.content.Intent
import android.os.Bundle
import android.widget.Toast

import androidx.appcompat.app.AppCompatActivity

import br.upf.deliveryapp.data.user.UserData
import br.upf.deliveryapp.databinding.ActivityLoginBinding

import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener

class LoginActivity : AppCompatActivity() {

    private lateinit var binding: ActivityLoginBinding
    private lateinit var firebaseDatabase: FirebaseDatabase
    private lateinit var databaseReference: DatabaseReference

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)

        firebaseDatabase = FirebaseDatabase.getInstance()
        databaseReference = firebaseDatabase.reference.child("users")

        binding.loginButton.setOnClickListener{
            val loginEmail = binding.loginEmail.text.toString()
            val loginPassword = binding.loginPassword.text.toString()
            if(loginEmail.isNotEmpty() && loginPassword.isNotEmpty()){
                loginUser(loginEmail, loginPassword)
            } else {
                Toast.makeText(this@LoginActivity, "Please fill all fields", Toast.LENGTH_LONG).show()
            }
        }

        binding.signupRedirect.setOnClickListener{
            startActivity(Intent(this@LoginActivity, SignupActivity::class.java))
            finish()
        }

    }

    private fun loginUser(email: String, password: String){
        databaseReference.orderByChild("email").equalTo(email).addListenerForSingleValueEvent(object: ValueEventListener{
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                if (dataSnapshot.exists()){
                    for (userSnapshot in dataSnapshot.children){
                        val userData = userSnapshot.getValue(UserData::class.java)
                        if (userData != null && userData.password == password){
                            if(userData.email.toString() == "admin@admin"){
                                Toast.makeText(this@LoginActivity, "Admin Login Successfully", Toast.LENGTH_SHORT).show()
                                startActivity(Intent(this@LoginActivity, AdminActivity::class.java))
                                finish()
                            }else{
                                Toast.makeText(this@LoginActivity, "Login Successfully", Toast.LENGTH_SHORT).show()
                                startActivity(Intent(this@LoginActivity, MainActivity::class.java))
                                finish()
                            }

                        }else{
                            Toast.makeText(this@LoginActivity, "Invalid Credentials", Toast.LENGTH_SHORT).show()

                        }

                }

            }
        }override fun onCancelled(databaseError: DatabaseError) {
                Toast.makeText(this@LoginActivity, "Database Error: ${databaseError.message}", Toast.LENGTH_SHORT).show()
            }
        }

        )
    }


}

