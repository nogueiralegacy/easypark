import 'package:flutter/material.dart';
import 'package:flutter_credit_card/flutter_credit_card.dart';

class PaymentPage extends StatefulWidget {
  const PaymentPage({super.key});

  @override
  State<PaymentPage> createState() => _PaymentPageState();
}

class _PaymentPageState extends State<PaymentPage> {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        CreditCardWidget(
          enableFloatingCard: true,
          floatingConfig: FloatingConfig(
            isGlareEnabled: true,
            isShadowEnabled: true,
            shadowConfig: FloatingShadowConfig(
              offset: Offset(5, 5),
              color: Colors.white.withOpacity(0.2),
              blurRadius: 8,
            ),
          ),
          cardNumber: '0830 4270 8563 2353',
          expiryDate: '07/30',
          cardHolderName: 'MATHEUS G MELO',
          cvvCode: '417',
          isHolderNameVisible: true,
          showBackView: false,
          obscureInitialCardNumber: true,
          glassmorphismConfig: Glassmorphism(
              blurX: 200,
              blurY: 200,
              gradient: LinearGradient(colors: [
                Color(0xff0A84FF),
                Color(0xff0A84FF).withOpacity(0.6),
                Colors.white.withOpacity(0.8)
              ])),
          onCreditCardWidgetChange: (CreditCardBrand cardBrand) {},
        ),
        SizedBox(
          height: 24,
        ),
        Container(
          margin: EdgeInsets.symmetric(horizontal: 16),
          height: 210,
          decoration: BoxDecoration(
              border: Border.all(width: 0.6, color: Colors.white),
              borderRadius: BorderRadius.circular(12)),
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text('+', style: TextStyle(fontSize: 32, ), ),
                Text('Adicionar cartão', style: TextStyle(fontSize: 18)),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
