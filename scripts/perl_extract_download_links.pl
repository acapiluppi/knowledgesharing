#!/usr/bin/perl -w

@all = `cat ALL_SAMPLE-links.csv`;
foreach $wget_link(@all){
        chomp $wget_link;
        if ($wget_link =~ m/ieeexplore/){
                # rename IEEE links
                # FROM: https://ieeexplore-ieee-org.proxy-ub.rug.nl/stamp/stamp.jsp?tp=&arnumber=6032441
                # TO: https://ieeexplore.ieee.org/abstract/document/6032441/
                $wget_link =~ s/https\:\/\/ieeexplore\.ieee\.org\/abstract\/document\//https\:\/\/ieeexplore\-ieee\-org\.proxy\-ub\.rug\.nl\/stamp\/stamp\.jsp\?tp\=\&arnumber\=/;
                $wget_link =~ s/\"//g;
                print "$wget_link\n";
        } elsif ($wget_link =~ /computer.org/){
                    # Rename computer.org links
                    # FROM: https://www.computer.org/csdl/proceedings-article/icse/2005/01553544/12OmNvzJG0p
                    # TO: https://www.computer.org/csdl/pds/api/csdl/proceedings/download-article/12OmNvzJG0p/pdf
#                     $wget_link = s/.*\//https\:\/\/www.computer.org\/csdl\/pds\/api\/csdl\/proceedings\/download-article\//;
                    #  s/$/\/pdf/;
                    #  print "$wget_link\n";
        } elsif($wget_link =~ /(dl.acm.org|dx.doi.org)/){
                $wget_link =~ s/.*\///;
                $wget_link =~ s/^/https\:\/\/dl-acm-org.proxy-ub.rug.nl\/doi\/pdf\/10.1145\//;
#                 https://dl-acm-org.proxy-ub.rug.nl/doi/pdf/10.1145/1095430.1081747
                $wget_link =~ s/\"//;
                print "$wget_link\n";
        } elsif($wget_link =~ /(\.pdf|\.PDF)/){
                # hard-coded
                $wget_link =~ s/\"//g;
                print "$wget_link\n";
        } elsif($wget_link =~ /link.springer.com/){
                $wget_link =~ s/.*\///;
                $wget_link =~ s/^/https:\/\/link.springer.com\/content\/pdf\/10.1007\//;
                $wget_link =~ s/$/\.pdf/;
                $wget_link =~ s/\"//;
                print "$wget_link\n";
        }
        else{
#                 print "$wget_link\n";
        }
}
