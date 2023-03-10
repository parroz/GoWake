

import 'package:flutter/material.dart';
import 'package:go_wake_app/utils/app_routes.dart';


class Splash extends StatefulWidget {
  const Splash({Key? key}) : super(key: key);

  @override
  State<Splash> createState() => _SplashState();
}

class _SplashState extends State<Splash> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(seconds: 2), () {
    _navigateToHome();
    });
  }
  _navigateToHome() async {
    Future.delayed(const Duration(seconds: 1), () {
      Navigator.of(context).pushNamed(
        AppRoutes.LOGIN,
        arguments: 'Currency Converter',
      );});
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Center(
            child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                mainAxisSize: MainAxisSize.max,
                children: [
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              mainAxisSize: MainAxisSize.max,
              children: [
                Container(

                    child: Image(
                        height: 200,
                        width: 200,
                        image: AssetImage('lib/assets/logo.png'))),
                Text('GoWake App'
                    '',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold))
              ]),
        ])));
  }
}
