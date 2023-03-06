import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../login/login_controller.dart';
import '../widgets/custom_textfield.dart';
import 'register_controller.dart';

import 'package:provider/provider.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({Key? key}) : super(key: key);

  @override
  RegisterPageState createState() => RegisterPageState();
}

class RegisterPageState extends State<RegisterPage> {
  final _formKeyValidator = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Material(
      child: Scaffold(
        body: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(40.0, 20.0, 40.0, 0.0),
          child: Consumer<RegisterController>(
              builder: (BuildContext context, controller, widget) {
            return Padding(
              padding: EdgeInsets.all(8.0),
              child: Form(
                key: _formKeyValidator,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: <Widget>[
                    Padding(
                      padding: EdgeInsets.only(right: 0, top: 60),
                      child: Text(
                        "Sign Up",
                        style: TextStyle(
                            fontWeight: FontWeight.bold, fontSize: 20),
                      ),

                    ),
                    SizedBox(
                      height: 5,
                    ),
                    CustomTextField(
                        label: "Username",
                        icon: Icons.supervised_user_circle,
                        input: TextInputType.text,
                        textController: controller.usernameController,
                        obscureText: false),
                    SizedBox(
                      height: 5,
                    ),
                    CustomTextField(
                        label: "Email",
                        icon: Icons.email_rounded,
                        input: TextInputType.text,
                        textController: controller.emailController,
                        obscureText: false),
                    SizedBox(
                      height: 5,
                    ),
                    CustomTextField(
                        label: "Password",
                        icon: Icons.lock_clock_rounded,
                        input: TextInputType.text,
                        textController: controller.passwordController,
                        obscureText: true),
                    SizedBox(
                      height: 5,
                    ),
                    CustomTextField(
                        label: "Confirm Password",
                        icon: Icons.lock_clock_rounded,
                        input: TextInputType.text,
                        textController: controller.password2Controller,
                        obscureText: true),
                    SizedBox(
                      height: 5,
                    ),
                    CustomTextField(
                        label: "Jury Code",
                        icon: Icons.verified_user,
                        input: TextInputType.text,
                        textController: controller.codeController,
                        obscureText: false),
                  ],
                ),
              ),
            );
          }),
        ),
      ),
    );
  }
}
