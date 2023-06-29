import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'custom_header_controller.dart';

class MyHeaderDrawer extends StatefulWidget {
  @override
  _MyHeaderDrawerState createState() => _MyHeaderDrawerState();
}

class _MyHeaderDrawerState extends State<MyHeaderDrawer> {


  @override
 void initState() {
    super.initState();
    var controller = Provider.of<HeaderController>(context, listen: false);
    controller.getCredentials();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Theme.of(context).colorScheme.background,
      width: double.infinity,
      height: 200,
      padding: EdgeInsets.only(top: 20.0),
      child: Consumer<HeaderController>(
        builder: (BuildContext context, controller, widget) {
       return Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              margin: EdgeInsets.only(bottom: 10),
              height: 70,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                image: DecorationImage(
                  image: AssetImage('lib/assets/user.png'),
                ),
              ),
            ),
            Text(
              controller.username,
              style: TextStyle(color: Theme.of(context).colorScheme.onSecondaryContainer, fontSize: 20),
            ),
            Text(
              controller.email,
              style: TextStyle(
                color: Theme.of(context).colorScheme.onSecondaryContainer,
                fontSize: 14,
              ),
            ),
          ],
        );
        }),
    );
  }
}
