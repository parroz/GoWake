import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import '../../shared/constants.dart';
import '../../utils/app_routes.dart';
import '../widgets/custom_button.dart';
import '../widgets/custom_textfield.dart';
import '../widgets/error_dialog.dart';
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
  void initState() {
    super.initState();
    var controller = Provider.of<RegisterController>(context, listen: false);
    controller.addListener(() {
      if (controller.state == LoginState.SUCCESS) {
        Navigator.of(context).pushNamed(
          AppRoutes.HOME,
        );
      }
      if (controller.state == LoginState.FAIL) {
        ShowErrorDialog(controller.errorMsg,context);
      }
    });
  }


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
                        obscureText: false,labelColor: Theme.of(context).colorScheme.primary,),
                    SizedBox(
                      height: 5,
                    ),
                    CustomTextField(
                        label: "Email",
                        icon: Icons.email_rounded,
                        input: TextInputType.text,
                        textController: controller.emailController,
                        obscureText: false,labelColor: Theme.of(context).colorScheme.primary,),
                    SizedBox(
                      height: 5,
                    ),
                    CustomTextField(
                        label: "Password",
                        icon: Icons.lock_clock_rounded,
                        input: TextInputType.text,
                        textController: controller.passwordController,
                        obscureText: true,
                        labelColor: Theme.of(context).colorScheme.primary,),
                    SizedBox(
                      height: 5,
                    ),
                TextFormField(
                  keyboardType: TextInputType.text,
                  controller:  controller.password2Controller,
                  obscureText: true,
                  onChanged: (value) {},
                  validator: (value) {
                    if (value!.isEmpty) {
                      return "Mandatory field";
                    }
                    if (controller.password2Controller.text !=controller.passwordController.text) {
                      return 'Entered passwords do not match.';
                    }
                  },
                  decoration: const InputDecoration(
                    labelText: "Confirm Password",
                    labelStyle: TextStyle(
                      color: Color(0xFFBE610D),
                    ),
                    suffixIcon: Icon(Icons.lock_clock_rounded,color:Color(0xFFB7BBC0)),
                  ),
                ),
              /*      CustomTextField(
                        label: "Confirm Password",
                        icon: Icons.lock_clock_rounded,
                        input: TextInputType.text,
                        textController: controller.password2Controller,
                        obscureText: true),*/
                    SizedBox(
                      height: 5,
                    ),
                    CustomTextField(
                        label: "Jury Code",
                        icon: Icons.verified_user,
                        input: TextInputType.text,
                        textController: controller.codeController,
                        obscureText: false,
                        labelColor:Theme.of(context).colorScheme.primary),
                    SizedBox(
                      height: 30,
                    ),
                    CustomButtom(
                      onPressed: () {
                        if (_formKeyValidator.currentState!.validate()) {
                          controller.register();
                        }
                      },
                      textcolor: Colors.white,
                      text: 'Continue',
                      backgroundcolor: const Color(0xFFCB6007),
                    ),
                    SizedBox(
                      height: 10,
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Text('Have an account?  ', style: TextStyle(
                      fontSize: 16,

                    ),),
                        GestureDetector(
                          onTap: () {
                            Navigator.of(context).pushNamed(
                              AppRoutes.LOGIN,
                            );
                          },
                          child: const Text(
                            "Sign In",
                            style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 16,
                                color: Color(0xFF044EA8),decoration: TextDecoration.underline,),
                          ),
                        )
                      ],
                    ),
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
