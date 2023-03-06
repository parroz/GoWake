import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

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
                      CustomTextField(
                          label: "Username",
                          icon: Icons.supervised_user_circle,
                          input: TextInputType.text,
                          textController: controller.usernameController,
                          obscureText: false),
                      const SizedBox(
                        height: 5,
                      ),
                      CustomTextField(
                          label: "Password",
                          icon: Icons.remove_red_eye_rounded,
                          input: TextInputType.text,
                          textController: controller.passwordController,
                          obscureText: true),
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
                          text: 'Continue',
                        ),
                      // ElevatedButton(
                      //   onPressed: () {
                      //     if (_formKeyValidator.currentState!.validate()) {
                      //       controller.login();
                      //     }
                      //   },
                      //   style: ElevatedButton.styleFrom(
                      //     primary: const Color(0xFF044EA8),
                      //     //backgroundColor: Theme.of(context).primaryColor,
                      //     foregroundColor: Colors.white,
                      //     padding: const EdgeInsets.symmetric(
                      //       horizontal: 30,
                      //       vertical: 8,
                      //     ),
                      //   ),
                      //   child: const Text(
                      //     'Sign In',
                      //   ),
                      // ),
                      const SizedBox(height: 40),
                      ElevatedButton(
                        onPressed: () => {
                          Navigator.of(context).pushNamed(
                            AppRoutes.REGISTER,
                          )
                        },
                        style: ElevatedButton.styleFrom(
                          primary: const Color(0xFFCB6007),
                          // backgroundColor: Theme.of(context).primaryColor,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(
                            horizontal: 30,
                            vertical: 8,
                          ),
                        ),
                        child: const Text(
                          'Sign Up',
                        ),
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
