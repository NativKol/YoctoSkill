<!-- Source: https://docs.yoctoproject.org/scarthgap/security-reference/reporting-vulnerabilities.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

#### 2 Reporting Vulnerabilities

The Yocto Project and OpenEmbedded are open-source, community-based projects used in numerous products. They assemble multiple other open-source projects, and need to handle security issues and practices both internal (in the code maintained by both projects), and external (maintained by other projects and organizations).

This manual assembles security-related information concerning the whole ecosystem. It includes information on reporting a potential security issue, the operation of the YP Security team and how to contribute in the related code. It is written to be useful for both security researchers and YP developers.

##### 2.1 How to report a potential security vulnerability?

If you would like to report a public issue (for example, one with a released CVE number), please report it using the Security Bugzilla.

If you are dealing with a not-yet-released issue, or an urgent one, please send a message to security AT yoctoproject DOT org, including as many details as possible: the layer or software module affected, the recipe and its version, and any example code, if available. This mailing list is monitored by the Yocto Project Security team.

For each layer, you might also look for specific instructions (if any) for reporting potential security issues in the specific `SECURITY.md` file at the root of the repository. Instructions on how and where submit a patch are usually available in `README.md`. If this is your first patch to the Yocto Project/OpenEmbedded, you might want to have a look into the Contributor’s Manual section “Preparing Changes for Submission”.

###### 2.1.1 Branches maintained with security fixes

See the Release process documentation for details regarding the policies and maintenance of stable branches.

The Releases page contains a list of all releases of the Yocto Project, grouped into current and previous releases. Previous releases are no longer actively maintained with security patches, but well-tested patches may still be accepted for them for significant issues.

###### 2.1.2 Security-related discussions at the Yocto Project

We have set up two security-related emails/mailing lists:

- Public Mailing List: yocto [dash] security [at] yoctoproject[dot] org

This is a public mailing list for anyone to subscribe to. This list is an open list to discuss public security issues/patches and security-related initiatives. For more information, including subscription information, please see the yocto-security mailing list info page.

This list requires moderator approval for new topics to be posted, to avoid private security reports to be posted by mistake.

- Yocto Project Security Team: security [at] yoctoproject [dot] org

This is an email for reporting non-published potential vulnerabilities. Emails sent to this address are forwarded to the Yocto Project Security Team members.

###### 2.1.3 What you should do if you find a security vulnerability

If you find a security flaw: a crash, an information leakage, or anything that can have a security impact if exploited in any Open Source software built or used by the Yocto Project, please report this to the Yocto Project Security Team. If you prefer to contact the upstream project directly, please send a copy to the security team at the Yocto Project as well. If you believe this is highly sensitive information, please report the vulnerability in a secure way, i.e. encrypt the email and send it to the private list. This ensures that the exploit is not leaked and exploited before a response/fix has been generated.

The Yocto Project ®

<docs@lists.yoctoproject.org>

Permission is granted to copy, distribute and/or modify this document under the terms of the Creative Commons Attribution-Share Alike 2.0 UK: England & Wales as published by Creative Commons.

To report any inaccuracies or problems with this (or any other Yocto Project) manual, or to send additions or changes, please send email/patches to the Yocto Project documentation mailing list at `docs@lists.yoctoproject.org` or log into the Libera Chat `#yocto` channel.

## Release Information

Release notes and migration guides for the different Yocto Project releases.
