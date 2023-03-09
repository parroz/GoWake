import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../shared/constants.dart';
import '../../utils/app_routes.dart';

import '../widgets/custom_button.dart';
import '../widgets/custom_textfield.dart';
import 'login_controller.dart';

class LoginScreen extends StatefulWidget {
  LoginScreen({Key? key}) : super(key: key);

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKeyValidator = GlobalKey<FormState>();

  @override
  void initState() {
    super.initState();
    var controller = Provider.of<LoginController>(context, listen: false);
    controller.addListener(() {
      if (controller.state == LoginState.SUCCESS) {
        Navigator.of(context).pushNamed(
          AppRoutes.HOME,
        );
      }
      if (controller.state == LoginState.FAIL) {
        _showErrorDialog(controller.errorMsg);
      }
    });
  }

  void _showErrorDialog(String msg) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Error!'),
        content: Text(msg),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Fechar'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Material(
      child: Scaffold(
        body: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(40.0, 50.0, 40.0, 0.0),
          child: Consumer<LoginController>(
              builder: (BuildContext context, controller, widget) {
            return Padding(
              padding: const EdgeInsets.all(8.0),
              child: Form(
                  key: _formKeyValidator,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: <Widget>[
                      const Image(
                          height: 200,
                          width: 200,
                          image: AssetImage('lib/assets/logo.png')),
                      const SizedBox(
                        height: 5,
                      ),
                      const Text(
                        "Sign In",
                        style: TextStyle(
                            fontWeight: FontWeight.bold, fontSize: 20),
                      ),
                      const SizedBox(
                        height: 5,
                      ),
                      CustomTextField(
                          label: "Username",
                          icon: Icons.supervised_user_circle,
                          input: TextInputType.text,
                          textController: controller.usernameController,
                          obscureText: false,
                          labelColor: Theme.of(context).colorScheme.primary),
                      const SizedBox(
                        height: 5,
                      ),
                      CustomTextField(
                          label: "Password",
                          icon: Icons.remove_red_eye_rounded,
                          input: TextInputType.text,
                          textController: controller.passwordController,
                          obscureText: true,
                          labelColor: Theme.of(context).colorScheme.primary),
                      const SizedBox(height: 20),
                      if (controller.state == LoginState.LOADING)
                        const Center(
                          child: CircularProgressIndicator(
                            valueColor:
                                AlwaysStoppedAnimation(Color(0xFF044EA8)),
                          ),
                        )
                      else
                        CustomButtom(
                          onPressed: () {
                            if (_formKeyValidator.currentState!.validate()) {
                              controller.login();
                            }
                          },
                          textcolor: Colors.white,
                          text: 'Continue',
                          backgroundcolor: const Color(0xFF044EA8),
                        ),
                      const SizedBox(
                        height: 3,
                      ),
                      GestureDetector(
                        onTap: () {

                        },
                        child: const Text(
                          "Forgot password",textAlign: TextAlign.center,
                          style: TextStyle(
                            fontSize: 14,
                            color: Color(0xFF044EA8),decoration: TextDecoration.underline,),
                        ),
                      ),    const SizedBox(height: 40),
                      CustomButtom(
                        onPressed: () => {
                          Navigator.of(context).pushNamed(
                            AppRoutes.REGISTER,
                          )
                        },
                        textcolor: Colors.white,
                        text: 'Sign Up',
                        backgroundcolor: const Color(0xFFCB6007),
                      ),
                    ],
                  )),
            );
          }),
        ),
      ),
    );
  }
}
