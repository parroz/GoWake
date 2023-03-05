import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:rx_notifier/rx_notifier.dart';

import '../../utils/app_routes.dart';
import '../test_page.dart';
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
          padding: EdgeInsets.fromLTRB(40.0, 50.0, 40.0, 0.0),
          child: Consumer<LoginController>(
              builder: (BuildContext context, controller, widget) {
            return Padding(
              padding: const EdgeInsets.all(8.0),
              child: Form(
                  key: _formKeyValidator,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: <Widget>[
                      Image(
                          height: 200,
                          width: 200,
                          image: AssetImage('lib/assets/logo.png')),
                      SizedBox(
                        height: 5,
                      ),
                      CustomTextField(
                          label: "Username",
                          icon: Icons.supervised_user_circle,
                          input: TextInputType.text,
                          controller: controller,
                          textController: controller.usernameController,
                          obscureText: false),
                      SizedBox(
                        height: 5,
                      ),
                      CustomTextField(
                          label: "Password",
                          icon: Icons.remove_red_eye_rounded,
                          input: TextInputType.text,
                          controller: controller,
                          textController: controller.passwordController,
                          obscureText: true),
                      SizedBox(height: 20),
                      if (controller.state == LoginState.LOADING)
                        const Center(
                          child: CircularProgressIndicator(
                            valueColor:
                                AlwaysStoppedAnimation(Color(0xFF044EA8)),
                          ),
                        )
                      else
                        ElevatedButton(
                          onPressed: () {
                            if (_formKeyValidator.currentState!.validate()) {
                              controller.login();
                            } },
                          style: ElevatedButton.styleFrom(
                            primary: const Color(0xFF044EA8),
                            //backgroundColor: Theme.of(context).primaryColor,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(
                              horizontal: 30,
                              vertical: 8,
                            ),
                          ),
                          child: Text(
                            'Sign In',
                          ),
                        ),
                      SizedBox(height: 40),
                      ElevatedButton(
                        onPressed: controller.login,
                        style: ElevatedButton.styleFrom(
                          primary: const Color(0xFFCB6007),
                          // backgroundColor: Theme.of(context).primaryColor,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(
                            horizontal: 30,
                            vertical: 8,
                          ),
                        ),
                        child: Text(
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

  CustomTextField(
      {required String label,
      required IconData icon,
      required TextInputType input,
      required LoginController controller,
      required TextEditingController textController,
      required bool obscureText}) {
    return TextFormField(
      keyboardType: input,
      controller: textController,
      obscureText: obscureText,
      onChanged: (value) {},
      validator: (value) {
        if (value!.isEmpty) {
          return "Mandatory field";
        }
      },
      decoration: InputDecoration(
        labelText: label,
        suffixIcon: Icon(icon),
      ),
    );
  }
}
