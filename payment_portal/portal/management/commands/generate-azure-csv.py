# import pandas as pd
# from django.core.management.base import BaseCommand

# class Command(BaseCommand):
#     help = "Generate Azure AD bulk user CSV from III Year student details Excel"

#     def handle(self, *args, **options):
#         input_file = r"C:\Users\HP\Documents\clg notes\sem7\cloud\project\payment_portal\portal\management\commands\student-details.xlsx"
#         output_file = r"C:\Users\HP\Documents\clg notes\sem7\cloud\project\payment_portal\portal\management\commands\azure-bulk-users.csv"

#         # Set your Azure default domain here
#         domain = "220701006rajalakshmiedu.onmicrosoft.com"

#         # Read only III Year sheet
#         df = pd.read_excel(input_file, sheet_name="III Year")
#         df = df[['Name', 'REGISTER NO']].dropna()
#         df.columns = ['Name', 'Roll']

#         # Generate username & email
#         df['Username'] = df['Roll'].astype(str) + f"@{domain}"
#         df['Block sign in'] = "No"
#         df['First Name'] = df['Name'].str.split().str[0]
#         df['Last Name'] = df['Name'].str.split().str[-1]
#         df['Initial Password'] = "ChangeMe@123"

#         # Reorder columns for Azure
#         final_df = df[[
#             'Username', 'Name', 'First Name', 'Last Name',
#             'Block sign in', 'Initial Password'
#         ]]

#         final_df.to_csv(output_file, index=False)
#         self.stdout.write(self.style.SUCCESS(f"Azure AD CSV generated: {output_file}"))


import pandas as pd
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Generate Azure AD bulk user CSV (III Year only) according to Microsoft template"

    def handle(self, *args, **options):
        input_file = r"C:\Users\HP\Documents\clg notes\sem7\cloud\project\payment_portal\portal\management\commands\student-details.xlsx"
        output_file = "azure_bulk_users2.csv"

        domain = "220701006rajalakshmiedu.onmicrosoft.com"

        # Read only III Year sheet
        df = pd.read_excel(input_file, sheet_name="III Year")
        df = df[['Name', 'REGISTER NO']].dropna()
        df.columns = ['Name', 'Roll']

        # Build required fields
        df['Name [displayName] Required'] = df['Name']
        df['User name [userPrincipalName] Required'] = df['Roll'].astype(str) + f"@{domain}"
        df['Initial password [passwordProfile] Required'] = "ChangeMe@123"
        df['Block sign in (Yes/No) [accountEnabled] Required'] = "No"
        df['First name [givenName]'] = df['Name'].str.split().str[0]
        df['Last name [surname]'] = df['Name'].str.split().str[-1]

        # Add empty columns for the rest of the template
        df['Job title [jobTitle]'] = ""
        df['Department [department]'] = ""
        df['Usage location [usageLocation]'] = ""
        df['Street address [streetAddress]'] = ""
        df['State or province [state]'] = ""
        df['Country or region [country]'] = ""
        df['Office [physicalDeliveryOfficeName]'] = ""
        df['City [city]'] = ""
        df['ZIP or postal code [postalCode]'] = ""
        df['Office phone [telephoneNumber]'] = ""
        df['Mobile phone [mobile]'] = ""

        # Reorder columns to match Azure template
        final_df = df[[
            'Name [displayName] Required',
            'User name [userPrincipalName] Required',
            'Initial password [passwordProfile] Required',
            'Block sign in (Yes/No) [accountEnabled] Required',
            'First name [givenName]',
            'Last name [surname]',
            'Job title [jobTitle]',
            'Department [department]',
            'Usage location [usageLocation]',
            'Street address [streetAddress]',
            'State or province [state]',
            'Country or region [country]',
            'Office [physicalDeliveryOfficeName]',
            'City [city]',
            'ZIP or postal code [postalCode]',
            'Office phone [telephoneNumber]',
            'Mobile phone [mobile]'
        ]]

        # Write CSV with version row
        with open(output_file, "w", encoding="utf-8", newline="") as f:
            f.write("version:v1.0\n")
            final_df.to_csv(f, index=False)

        self.stdout.write(self.style.SUCCESS(f"Azure AD CSV generated: {output_file}"))
