import 'package:flutter/material.dart';
// import 'package:faker/faker.dart';

// final faker = Faker();

class UserProfile {
  final String name;
  final String email;
  final String cpf;
  // final String avatarUrl;

  UserProfile({
    required this.name,
    required this.email,
    required this.cpf,
    // required this.avatarUrl,
  });
}

final mockUser = UserProfile(
  name: "Matheus G de Melo",
  email: "matheusgerlo@gmail.com",
  cpf: "701.725.511-96",
);

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.fromLTRB(16.0, 24, 16, 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: CircleAvatar(
                radius: 100,
                backgroundImage: Image.asset('assets/avatar_image.png').image,
              ),
            ),
            SizedBox(height: 16),
            Text(
              mockUser.name,
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            Text(
              mockUser.email,
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
            SizedBox(height: 16),
            Text(
              mockUser.cpf,
              style: TextStyle(fontSize: 16),
              textAlign: TextAlign.center,
            ),
            Spacer(),
            SizedBox(
              width: double.maxFinite,
              child: ElevatedButton(
                onPressed: () {
                  // Handle logout logic here
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.red,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
                child: Text(
                  'Logout',
                  style: TextStyle(color: Colors.white),
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
